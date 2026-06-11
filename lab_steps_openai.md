# Hướng dẫn thực hành Lab 11 (Phiên bản OpenAI)

### 1. Mục tiêu của bài thực hành (Lab)
Mục tiêu chính là xây dựng một ứng dụng AI an toàn bằng cách thiết lập các "rào chắn" (guardrails) và quy trình có con người tham gia (HITL - Human in the Loop). Bạn sẽ phải làm việc với các hệ thống phòng thủ như: input guardrails, output guardrails, cấu hình NeMo Guardrails và thiết kế workflow HITL.

### 2. Các bước Setup Môi Trường
Bạn có 3 lựa chọn để chạy dự án:

**Cách 1: Chạy trên Google Colab (Được khuyến nghị)**
1. Tải file `notebooks/lab11_guardrails_hitl.ipynb` lên Google Colab.
2. Tạo API Key tại trang quản lý API của OpenAI (platform.openai.com).
3. Lưu API key vào mục Secrets của Colab với tên `OPENAI_API_KEY`.
4. Chạy tuần tự các ô code (cell) trong notebook.

**Cách 2: Chạy Jupyter Notebook ở máy cá nhân (Local)**
1. Cài đặt thư viện: `pip install -r requirements.txt`
2. Cài đặt biến môi trường: `export OPENAI_API_KEY="your-openai-api-key-here"`
3. Mở notebook: `jupyter notebook notebooks/lab11_guardrails_hitl.ipynb`

**Cách 3: Chạy trực tiếp mã nguồn Python (Local)**
1. Di chuyển vào thư mục code: `cd src/`
2. Cài đặt thư viện: `pip install -r ../requirements.txt`
3. Cài đặt biến môi trường: `export OPENAI_API_KEY="your-openai-api-key-here"`
4. Bạn có thể chạy toàn bộ bài lab bằng lệnh `python main.py`, hoặc chạy từng phần bằng flag `--part` (ví dụ: `python main.py --part 1`).

### 3. Lộ trình thực hành (Gồm 4 phần chính - Dự kiến 2.5 giờ)
Bạn sẽ phải đi qua 4 phần nội dung để hoàn thiện bài lab này, tương ứng với việc giải quyết **13 TODOs (nhiệm vụ)**:

*   **Phần 1: Tấn công (Attacks) & Red Teaming (30 phút)**
    *   Tấn công thử vào một Agent chưa được bảo vệ.
    *   Sử dụng AI (OpenAI) để tự động sinh ra các test case tấn công (AI Red Teaming).
    *   *(Bao gồm TODO 1, 2)*
*   **Phần 2: Xây dựng Rào chắn bảo vệ - Guardrails (60 phút)**
    *   **2A:** Code Input Guardrails để phát hiện injection và lọc chủ đề. *(Bao gồm TODO 3, 4, 5)*
    *   **2B:** Code Output Guardrails để lọc nội dung (PII, secret) và dùng chính LLM làm giám khảo (LLM-as-Judge). *(Bao gồm TODO 6, 7, 8)*
    *   **2C:** Cấu hình NeMo Guardrails của NVIDIA sử dụng ngôn ngữ Colang. *(Bao gồm TODO 9)*
*   **Phần 3: Kiểm thử tự động - Testing Pipeline (30 phút)**
    *   Thực hiện lại 5 cuộc tấn công ban đầu nhưng vào hệ thống đã gắn Guardrails để so sánh trước/sau.
    *   Xây dựng một pipeline kiểm thử bảo mật tự động.
    *   *(Bao gồm TODO 10, 11)*
*   **Phần 4: Thiết kế luồng HITL - Human In The Loop (30 phút)**
    *   Code một bộ định tuyến dựa trên độ tin cậy (Confidence Router).
    *   Thiết kế 3 điểm ra quyết định có sự can thiệp của con người.
    *   *(Bao gồm TODO 12, 13)*

### 4. Kết quả đầu ra cần nộp (Deliverables)
Sau khi hoàn thành 13 TODOs ở các bước trên, bạn cần có 2 sản phẩm cuối cùng để báo cáo/nộp bài:
1. **Security Report:** Bản báo cáo so sánh kết quả của ít nhất 5 cuộc tấn công trước và sau khi gắn hệ thống bảo vệ (ADK + NeMo).
2. **HITL Flowchart:** Sơ đồ luồng (flowchart) thể hiện 3 điểm quyết định có con người can thiệp kèm theo các con đường leo thang xử lý (escalation paths).
