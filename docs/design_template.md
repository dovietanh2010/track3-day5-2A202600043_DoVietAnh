# Design Template: Multi-Agent Research System

## Problem

Hệ thống cần xử lý các yêu cầu nghiên cứu chuyên sâu (Research Queries) từ người dùng. Các yêu cầu này thường phức tạp, đòi hỏi phải tìm kiếm thông tin từ nhiều nguồn, phân tích dữ liệu đa chiều và tổng hợp thành báo cáo chuyên nghiệp có trích dẫn.

## Why multi-agent?

Single-agent (một LLM duy nhất) thường gặp các vấn đề sau:
- **Giới hạn context window**: Khó xử lý khối lượng lớn tài liệu tìm kiếm được.
- **Thiếu tính phản biện**: Dễ bị "hallucination" hoặc đưa ra câu trả lời hời hợt.
- **Khó kiểm soát quy trình**: Khó can thiệp vào giữa quá trình tìm kiếm và viết bài.

Multi-agent cho phép chia nhỏ bài toán: một agent chuyên tìm kiếm, một agent chuyên phân tích phản biện, và một agent chuyên viết lách, dưới sự điều phối của Supervisor.

## Agent roles

| Agent | Responsibility | Input | Output | Failure mode |
|---|---|---|---|---|
| **Supervisor** | Điều phối toàn bộ quy trình, ra quyết định chọn agent tiếp theo. | Query & Current State | Next Agent Name | Vòng lặp vô tận (đã chặn bằng max_iterations). |
| **Researcher** | Tìm kiếm thông tin từ web (Tavily) và viết ghi chú. | Query | Research Notes & Sources | Không tìm thấy thông tin (đã có fallback mock). |
| **Analyst** | Phân tích ghi chú nghiên cứu, tìm lỗ hổng và mâu thuẫn. | Research Notes | Analysis Insights | Phân tích quá chung chung. |
| **Writer** | Tổng hợp tất cả thông tin thành báo cáo cuối cùng. | Notes & Analysis | Final Report | Thiếu trích dẫn (đã có Prompt guideline). |
| **Critic** | (Bonus) Kiểm tra tính xác thực và an toàn của báo cáo. | Final Report | Feedback/Approval | Quá khắt khe làm chậm quy trình. |

## Shared state

Hệ thống sử dụng `ResearchState` kế thừa từ Pydantic:
- `request`: Lưu query và yêu cầu của người dùng.
- `sources`: Danh sách các link và nội dung thu thập được.
- `research_notes`: Ghi chú thô từ Researcher.
- `analysis_notes`: Phân tích sâu từ Analyst.
- `final_answer`: Bài báo cáo hoàn chỉnh.
- `iteration`: Đếm số bước để tránh lặp vô hạn.

## Routing policy

Sử dụng **LangGraph** với cấu trúc đồ thị:
1. `Start` -> `Supervisor`
2. `Supervisor` -> (`Researcher` | `Analyst` | `Writer` | `End`) dựa trên LLM Reasoning.
3. Sau mỗi Worker -> Quay lại `Supervisor`.
4. Nếu báo cáo đã xong -> `End`.

## Guardrails

- **Max iterations**: 10 (Chặn đứng việc Agent nói chuyện với nhau quá lâu).
- **Timeout**: Được quản lý bởi LangGraph.
- **Retry**: Sử dụng thư viện `tenacity` với exponential backoff cho LLM calls.
- **Fallback**: Nếu Tavily API lỗi, hệ thống sử dụng Mock Search để không bị crash.
- **Validation**: Critic Agent kiểm tra lại chất lượng trước khi kết thúc.

## Benchmark plan

- **Query**: "Applications of GraphRAG in business"
- **Metrics**: 
  - Latency (giây)
  - Answer Length (số ký tự)
  - Cost (USD)
- **Expected Outcome**: Multi-agent sẽ chậm hơn và đắt hơn nhưng bài viết sẽ dài hơn, có cấu trúc tốt hơn và sâu sắc hơn so với bản Single-agent.
