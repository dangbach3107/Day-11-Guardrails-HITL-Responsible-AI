"""
OpenAI Wrapper to replace Google ADK and GenAI SDK.
This provides the same interface so we don't have to rewrite the lab's logic structure.
"""
import uuid
import os
import asyncio
from typing import List, Optional, Any
from dataclasses import dataclass

try:
    from openai import AsyncOpenAI
except ImportError:
    pass  # Will be installed via pip

# =============================================================================
# Types mapping (Google GenAI style)
# =============================================================================
class Part:
    def __init__(self, text: str):
        self.text = text

    @classmethod
    def from_text(cls, text: str):
        return cls(text=text)

class Content:
    def __init__(self, role: str, parts: List[Part]):
        self.role = role
        self.parts = parts

class types:
    Part = Part
    Content = Content

# =============================================================================
# Agent Components
# =============================================================================
class LlmAgent:
    def __init__(self, model: str, name: str, instruction: str):
        # We override the model to use the one requested by user
        self.model = "gpt-4o-mini" 
        self.name = name
        self.instruction = instruction

class Session:
    def __init__(self, id: str):
        self.id = id
        self.history = []

class SessionService:
    def __init__(self):
        self.sessions = {}

    async def get_session(self, app_name: str, user_id: str, session_id: str):
        if session_id in self.sessions:
            return self.sessions[session_id]
        raise ValueError("Session not found")

    async def create_session(self, app_name: str, user_id: str):
        session = Session(id=str(uuid.uuid4()))
        self.sessions[session.id] = session
        return session

class BasePlugin:
    def __init__(self, name: str):
        self.name = name

    async def on_user_message_callback(self, *, invocation_context, user_message: Content) -> Optional[Content]:
        return None

    async def after_model_callback(self, *, callback_context, llm_response) -> Any:
        return llm_response

class LLMResponseMock:
    """Mock for the response object that ADK returns in after_model_callback"""
    def __init__(self, content: Content):
        self.content = content

class EventMock:
    """Mock for the event object yielded by the runner"""
    def __init__(self, content: Content):
        self.content = content

class InMemoryRunner:
    def __init__(self, agent: LlmAgent, app_name: str, plugins: List[BasePlugin] = None):
        self.agent = agent
        self.app_name = app_name
        self.plugins = plugins or []
        self.session_service = SessionService()

    async def run_async(self, user_id: str, session_id: str, new_message: Content):
        session = await self.session_service.get_session(self.app_name, user_id, session_id)
        
        # 1. Run Input Plugins
        plugin_message = new_message
        for plugin in self.plugins:
            if hasattr(plugin, "on_user_message_callback"):
                result = await plugin.on_user_message_callback(
                    invocation_context=None, user_message=plugin_message
                )
                if result is not None:
                    # Input blocked! Return the blocked message immediately
                    yield EventMock(content=result)
                    return
        
        # Extract text from the message
        user_text = ""
        for p in plugin_message.parts:
            user_text += p.text

        # Add to history
        session.history.append({"role": "user", "content": user_text})

        # 2. Call OpenAI API
        client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY", "dummy"))
        
        messages = [{"role": "system", "content": self.agent.instruction}]
        messages.extend(session.history)

        try:
            response = await client.chat.completions.create(
                model=self.agent.model,
                messages=messages,
                temperature=0.7,
            )
            bot_text = response.choices[0].message.content
        except Exception as e:
            bot_text = f"API Error: {e}"

        # 3. Output Plugins
        llm_response = LLMResponseMock(content=Content(role="model", parts=[Part(text=bot_text)]))
        for plugin in self.plugins:
            if hasattr(plugin, "after_model_callback"):
                llm_response = await plugin.after_model_callback(
                    callback_context=None, llm_response=llm_response
                )
        
        final_bot_text = ""
        for p in llm_response.content.parts:
            final_bot_text += p.text
            
        session.history.append({"role": "assistant", "content": final_bot_text})
        yield EventMock(content=llm_response.content)

class InvocationContext:
    pass

# Export these so that imports like `from google.adk.plugins import base_plugin` can be mapped easily.
base_plugin = type("base_plugin", (), {"BasePlugin": BasePlugin})
llm_agent = type("llm_agent", (), {"LlmAgent": LlmAgent})
runners = type("runners", (), {"InMemoryRunner": InMemoryRunner})
