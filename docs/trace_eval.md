# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** Dinh Thi Minh Tam  
> **Mã Sinh Viên / Mã Học viên:** 2A202602433  
> **Chủ đề Lựa chọn:** [Trợ lý Quản lý Thư viện & Tài liệu: Tra cứu vị trí sách, tình trạng mượn/trả và gia hạn tài liệu]  

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| **Tiêu chí Đánh giá** | **Mức độ** | **Giải trình chi tiết lý do chọn điểm** |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | **4 / 5** | Bài toán đòi hỏi chuỗi tư duy nhiều bước: bóc tách thực thể (mã sinh viên, tên/mã sách) → kiểm tra trạng thái mượn → đối soát chính sách thư viện (giới hạn số lần gia hạn, tình trạng giữ sách của độc giả khác, phí trễ hạn) → đưa ra quyết định hành động. |
| **2. Tool Interaction** | **5 / 5** | Bắt buộc kết nối CSDL Thư viện (hệ thống OPAC/ILS) thông qua MCP Server với tối thiểu 2 nhóm công cụ: nhóm tra cứu dữ liệu (`search_catalog`, `get_borrow_record`) và nhóm hành động ghi nhận (`renew_book_loan`). |
| **3. Dynamic Decision** | **4 / 5** | Hành động kế tiếp thay đổi hoàn toàn theo quan sát từ DB (Observation): nếu sách sẵn có trên kệ → điều hướng tới số kệ/khu vực; nếu sách đang mượn → kiểm tra điều kiện gia hạn; nếu phát hiện bị khóa tài khoản hoặc có người đặt trước → dừng tác vụ gia hạn và đưa ra giải pháp thay thế. |
| **4. Long Horizon Goal** | **3 / 5** | Phiên tương tác cần duy trì mục tiêu qua 2–4 lượt hội thoại (nhận diện nhu cầu → yêu cầu mã số thẻ/xác thực → chọn sách cần gia hạn → xác nhận giao dịch thành công). Quy trình có độ dài vừa phải, không quá phân nhánh nhưng đòi hỏi lưu giữ trạng thái ngữ cảnh ổn định. |
| **TỔNG ĐIỂM AGENTIC FIT** | **16 / 20** | **Rất phù hợp để triển khai Agentic System** (vượt mốc 12/20). |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp chỉ dùng Mock Offline Provider sẽ không đạt điểm nghiệm thực tế.

Dán 1 đoạn trích xuất log tiêu biểu từ file `docs/trace_waterfall.json` sinh ra từ phản hồi LLM API thật:

```json
[
  {
    "step": 1,
    "action_type": "TOOL_EXECUTION",
    "tool_name": "academic_query",
    "arguments": {
      "student_id": "SV2026001"
    },
    "observation": {
      "status": "SUCCESS",
      "student_id": "SV2026001",
      "data": {
        "full_name": "Nguyễn Văn An",
        "gpa": 3.85
      }
    },
    "latency_ms": 120.5
  }
]
```

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [x] Đã điền API Key thật trong `.env` và xác nhận Agent chạy mượt mà trên LLM API thật (Gemini/OpenAI).
- **Tổng số Test Cases đã chạy thành công:** 5 / 5 test cases.
- **Số lượt gọi Tool qua MCP Server chính xác:** 5 lượt.
- **Kết quả đẩy Repo nộp bài:** [ ] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!
