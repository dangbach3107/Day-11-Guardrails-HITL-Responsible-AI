# Sơ đồ luồng HITL (Human-in-the-Loop Flowchart)

Sơ đồ dưới đây minh hoạ bộ định tuyến Confidence Router và 3 điểm quyết định có con người can thiệp (HITL Decision Points) trong hệ thống AI của VinBank, bao gồm các con đường leo thang xử lý (escalation paths).

```mermaid
flowchart TD
    Start([User Request / Agent Task]) --> Router{Confidence Router}
    
    %% Routing Logic
    Router -- "High Risk Action<br>(Transfer, Close Account) <br>OR Confidence < 0.7" --> Escalate["Escalation Queue<br>High Priority"]
    Router -- "0.7 <= Confidence < 0.9" --> ReviewQueue["Review Queue<br>Normal Priority"]
    Router -- "Confidence >= 0.9" --> AutoSend(["Auto-Send / Execute Action"])

    %% HITL DP 1: High-Value Transaction (Human-in-the-loop)
    Escalate -- "Transfer > $10,000" --> DP1{"DP1: High-Value Transaction<br>(Human-in-the-Loop)"}
    DP1 -- Approve --> AutoSend
    DP1 -- Reject --> Block(["Action Blocked / User Notified"])
    DP1 -- Suspicious --> SecTeam(["Security Team / Fraud Dept"])

    %% HITL DP 3: Ambiguous Policy Question (Human-as-tiebreaker)
    ReviewQueue -- "Loan Policy Query" --> DP3{"DP3: Ambiguous Policy<br>(Human-as-Tiebreaker)"}
    DP3 -- "Selects Best LLM Answer" --> AutoSend
    DP3 -- "Manually Drafts Answer" --> AutoSend

    %% HITL DP 2: Suspicious Activity (Human-on-the-loop)
    AutoSend --> AuditLog[("Audit Log / Monitoring")]
    AuditLog -- "Failed Logins + Pwd Reset" --> DP2{"DP2: Suspicious Activity<br>(Human-on-the-Loop)"}
    DP2 -- "Review Reveals Fraud" --> Suspend(["Suspend Account / Freeze Assets"])
    DP2 -- "False Alarm" --> Archive(["Archive / Resolve Alert"])

    %% Styling
    classDef escalate fill:#ffcccc,stroke:#ff0000,stroke-width:2px;
    classDef review fill:#fff3cd,stroke:#ffc107,stroke-width:2px;
    classDef auto fill:#d4edda,stroke:#28a745,stroke-width:2px;
    classDef dp fill:#e2d9f3,stroke:#6f42c1,stroke-width:2px;
    
    class Escalate,SecTeam,Block,Suspend escalate;
    class ReviewQueue review;
    class AutoSend auto;
    class DP1,DP2,DP3 dp;
```

## Chi tiết 3 điểm quyết định (Decision Points)

1. **DP1: High-Value Transaction Review (Human-in-the-loop)**
   - **Trigger:** Người dùng yêu cầu chuyển khoản trên $10,000. Lệnh này nằm trong danh sách rủi ro cao (High Risk) nên bị đẩy thẳng vào hàng đợi Escalation.
   - **Xử lý:** Giao dịch bị chặn lại cho đến khi nhân viên (Human) vào xem xét bối cảnh (Context: Lịch sử tài khoản, IP,...) rồi quyết định Approve, Reject, hoặc báo cáo Fraud.

2. **DP2: Suspicious Account Activity (Human-on-the-loop)**
   - **Trigger:** Hệ thống giám sát (Audit Log) nhận thấy Agent ghi nhận nhiều lần đăng nhập sai mật khẩu kèm theo một lệnh reset mật khẩu từ một IP lạ.
   - **Xử lý:** Agent vẫn xử lý yêu cầu (Auto-send), nhưng cảnh báo được sinh ra ngầm cho nhân viên bảo mật (Human) theo dõi. Nếu nhân viên phát hiện bất thường, họ sẽ đóng băng tài khoản sau đó.

3. **DP3: Ambiguous Policy Question (Human-as-tiebreaker)**
   - **Trigger:** Người dùng hỏi một câu phức tạp về chính sách vay vốn mà AI chỉ đạt điểm tự tin (Confidence) ở mức trung bình (ví dụ 0.8).
   - **Xử lý:** Câu trả lời không gửi đi ngay mà đưa vào Review Queue. Một nhân viên (Human) sẽ vào đọc câu hỏi, xem 2 phương án trả lời do AI gợi ý, và chọn phương án đúng nhất (Tiebreaker) hoặc tự soạn lại câu trả lời.
