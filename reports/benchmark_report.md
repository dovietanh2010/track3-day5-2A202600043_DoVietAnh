# Báo cáo Đánh giá Hệ thống: Multi-Agent vs. Single-Agent

## 1. Tóm tắt điều hành
Báo cáo này đánh giá hiệu năng và chất lượng của hệ thống **Multi-Agent Research Lab**. Chúng tôi so sánh mô hình **Single-Agent Baseline** truyền thống và hệ thống **Multi-Agent dựa trên LangGraph** với câu hỏi: *"Applications of GraphRAG in business"*.

## 2. Số liệu định lượng

| Chỉ số | Baseline (Single-Agent) | Hệ thống Multi-Agent | Sự khác biệt |
| :--- | :--- | :--- | :--- |
| **Thời gian phản hồi** | 9.29s | 36.65s | +294.5% |
| **Chi phí ước tính** | $0.0100 | $0.0500 | +400.0% |
| **Độ dài bài viết** | 3880 ký tự | 6357 ký tự | +63.8% |
| **Số bước xử lý** | 1 | 4 | +3 bước |
| **Điểm chất lượng (1-10)** | 8.88/10 | 10.0/10 | +1.22 điểm |

*trace: reports/multi_agent_research.png và single_agent_research.png*

## 3. Phân tích định tính

### 3.1. Hiệu năng của Baseline
- **Độ sâu**: Chỉ tóm tắt được bề mặt thông tin, thiếu sự kết nối logic sâu sắc giữa các nguồn.
- **Cấu trúc**: Phẳng, thường là các đoạn văn bản liệt kê thông tin cơ bản.
- **Trích dẫn**: Có trích dẫn nhưng đôi khi không khớp chính xác với nội dung.

### 3.2. Hiệu năng của Hệ thống Multi-Agent
- **Độ sâu**: Sâu sắc hơn đáng kể nhờ có bước phân tích của Analyst để tìm ra các góc nhìn chuyên sâu.
- **Cấu trúc**: Chuyên nghiệp với các phần mở đầu, nội dung chi tiết và kết luận mạch lạc.
- **Độ tin cậy**: Tích hợp các Agent kiểm soát (Critic/Supervisor) giúp giảm thiểu sai sót thông tin.

## 4. Phân tích lỗi và Cách khắc phục (Failure Mode Analysis)

| Tình huống lỗi | Tác động | Giải pháp khắc phục |
| :--- | :--- | :--- |
| **Vòng lặp Supervisor** | Các Agent đẩy việc cho nhau mãi không dừng. | **Fix**: Giới hạn cứng `max_iterations=10`. |
| **Ảo giác tìm kiếm** | LLM tự bịa ra thông tin khi thiếu dữ liệu. | **Fix**: Researcher chỉ được dùng thông tin từ `SourceDocument` thực tế. |
| **Tràn ngữ cảnh** | Quá nhiều kết quả tìm kiếm làm vượt giới hạn LLM. | **Fix**: Giới hạn `max_sources=5` và nén thông tin qua Researcher Notes. |
| **Lỗi API mạng** | API Tavily hoặc OpenAI bị lỗi hoặc timeout. | **Fix**: Tích hợp `tenacity` để tự động thử lại (retry). |

## 5. Kết luận
Hệ thống **Multi-Agent** vượt trội hoàn toàn về chất lượng nghiên cứu, mặc dù chậm và tốn kém hơn. Đây là sự đánh đổi xứng đáng cho các tác vụ quan trọng.

---
*Báo cáo được tạo tự động bởi scripts/run_benchmarks.py*
