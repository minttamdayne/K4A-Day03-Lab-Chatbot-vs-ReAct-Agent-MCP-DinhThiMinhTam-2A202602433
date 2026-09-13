"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer phục vụ cho MCP Server.
"""

import json
from typing import Dict, Any

# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA (TASK 1.2)
# ==============================================================================

TOOLS_SCHEMA = [
    # Tool 1: Đã được định nghĩa mẫu sẵn cho Học viên tham khảo
    {
        "name": "academic_query",
        "description": "Tra cứu hồ sơ và thông tin học vụ của sinh viên VinUni bằng mã sinh viên.",
        "parameters": {
            "type": "object",
            "properties": {
                "student_id": {
                    "type": "string",
                    "description": "Mã sinh viên cần tra cứu (ví dụ: 'SV2026001')"
                }
            },
            "required": ["student_id"]
        }
    },
    
    {
        "name": "schedule_appointment",
        "description": "Đặt lịch hẹn tư vấn học vụ với Cố vấn học tập VinUni.",
        "parameters": {
            "type": "object",
            "properties": {
                "student_id": {
                    "type": "string",
                    "description": "Mã sinh viên cần đặt lịch (ví dụ: 'SV2026001')"
                },
                "datetime_str": {
                    "type": "string",
                    "description": "Thời gian hẹn (ví dụ: '14:00 15/09/2026')"
                },
                "advisor_name": {
                    "type": "string",
                    "description": "Tên cố vấn học tập"
                }
            },
            "required": ["student_id", "datetime_str", "advisor_name"]
        }
    },
    {
        "name": "search_catalog",
        "description": "Tra cứu tình trạng còn sách và vị trí kệ theo tên tài liệu trong thư viện.",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Tên sách cần tìm"}
            },
            "required": ["title"]
        }
    },
    {
        "name": "get_borrow_record",
        "description": "Lấy danh sách sách đang mượn và điều kiện gia hạn của một sinh viên.",
        "parameters": {
            "type": "object",
            "properties": {
                "student_id": {"type": "string", "description": "Mã sinh viên"}
            },
            "required": ["student_id"]
        }
    },
    {
        "name": "renew_book_loan",
        "description": "Gia hạn một lượt mượn sách sau khi đã kiểm tra và xác nhận đủ điều kiện.",
        "parameters": {
            "type": "object",
            "properties": {
                "student_id": {"type": "string", "description": "Mã sinh viên"},
                "loan_id": {"type": "string", "description": "Mã lượt mượn lấy từ get_borrow_record"}
            },
            "required": ["student_id", "loan_id"]
        }
    }
]

# ==============================================================================
# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

MOCK_DATABASE = {
    "SV2026001": {
        "full_name": "Nguyễn Văn An",
        "class": "AI-K4",
        "gpa": 3.85,
        "email": "an.nv@vinuni.edu.vn",
        "status": "Đang học",
        "advisor": "PGS.TS Nguyễn Văn A"
    },
    "SV2026002": {
        "full_name": "Trần Thị Bình",
        "class": "AI-K4",
        "gpa": 3.60,
        "email": "binh.tt@vinuni.edu.vn",
        "status": "Đang học",
        "advisor": "TS. Lê Thị B"
    }
}

CATALOG_DATABASE = {
    "tôi thấy hoa vàng trên cỏ xanh": {
        "title": "Tôi thấy hoa vàng trên cỏ xanh",
        "author": "Nguyễn Nhật Ánh",
        "available_copies": 2,
        "total_copies": 4,
        "shelf": "Kệ VHVN-03, Tầng 2"
    }
}

BORROW_DATABASE = {
    "SV202602433": [
        {
            "loan_id": "LN-2433-01",
            "title": "Cho tôi xin một vé về tuổi thơ",
            "due_date": "20/09/2026",
            "renewal_count": 0,
            "overdue": False,
            "reserved_by_another": False,
            "renewable": True
        }
    ],
    "SV20260110": [
        {
            "loan_id": "LN-0110-01",
            "title": "Ngày xưa có một chuyện tình",
            "due_date": "10/09/2026",
            "renewal_count": 0,
            "overdue": True,
            "reserved_by_another": True,
            "renewable": False,
            "renewal_denial_reason": "Sách đã quá hạn và đang được độc giả khác đặt trước."
        }
    ]
}


def execute_academic_query(student_id: str) -> str:
    """Thực thi tra cứu học vụ theo mã sinh viên"""
    student = MOCK_DATABASE.get(student_id.strip().upper())
    if student:
        return json.dumps({
            "status": "SUCCESS",
            "student_id": student_id,
            "data": student
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy dữ liệu sinh viên có mã '{student_id}'"
        }, ensure_ascii=False)


def execute_schedule_appointment(student_id: str, datetime_str: str, advisor_name: str = "PGS.TS Nguyễn Văn A") -> str:
    """Thực thi đặt lịch hẹn tư vấn học vụ"""
    return json.dumps({
        "status": "SUCCESS",
        "booking_id": f"BK-{student_id}-99",
        "student_id": student_id,
        "datetime": datetime_str,
        "advisor": advisor_name,
        "message": f"Đặt lịch thành công cho sinh viên {student_id} với {advisor_name} vào lúc {datetime_str}."
    }, ensure_ascii=False)


def execute_search_catalog(title: str) -> str:
    """Tra cứu sách không phân biệt hoa thường."""
    normalized_title = title.strip().lower()
    book = next((data for key, data in CATALOG_DATABASE.items()
                 if normalized_title in key or key in normalized_title), None)
    if not book:
        return json.dumps({"status": "NOT_FOUND", "message": f"Không tìm thấy sách '{title}'."}, ensure_ascii=False)
    return json.dumps({"status": "SUCCESS", "data": book}, ensure_ascii=False)


def execute_get_borrow_record(student_id: str) -> str:
    """Lấy các lượt mượn hiện tại của sinh viên."""
    normalized_id = student_id.strip().upper()
    loans = BORROW_DATABASE.get(normalized_id)
    if loans is None:
        return json.dumps({"status": "NOT_FOUND", "message": f"Không có hồ sơ mượn cho '{student_id}'."}, ensure_ascii=False)
    return json.dumps({"status": "SUCCESS", "student_id": normalized_id, "loans": loans}, ensure_ascii=False)


def execute_renew_book_loan(student_id: str, loan_id: str) -> str:
    """Gia hạn sách nếu lượt mượn tồn tại và đủ điều kiện."""
    normalized_id = student_id.strip().upper()
    loan = next((item for item in BORROW_DATABASE.get(normalized_id, []) if item["loan_id"] == loan_id), None)
    if not loan:
        return json.dumps({"status": "NOT_FOUND", "message": f"Không tìm thấy lượt mượn '{loan_id}'."}, ensure_ascii=False)
    if not loan.get("renewable"):
        reason = loan.get("renewal_denial_reason", "Lượt mượn không đủ điều kiện gia hạn.")
        return json.dumps({"status": "REJECTED", "loan_id": loan_id, "message": reason}, ensure_ascii=False)
    loan["renewal_count"] += 1
    loan["due_date"] = "27/09/2026"
    return json.dumps({
        "status": "SUCCESS", "student_id": normalized_id, "loan_id": loan_id,
        "title": loan["title"], "new_due_date": loan["due_date"],
        "message": f"Đã gia hạn '{loan['title']}' đến ngày {loan['due_date']}."
    }, ensure_ascii=False)


# Router gọi tool thực tế
TOOL_ROUTER = {
    "academic_query": execute_academic_query,
    "schedule_appointment": execute_schedule_appointment,
    "search_catalog": execute_search_catalog,
    "get_borrow_record": execute_get_borrow_record,
    "renew_book_loan": execute_renew_book_loan
}

def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Hàm trung chuyển thực thi tool"""
    if tool_name in TOOL_ROUTER:
        try:
            return TOOL_ROUTER[tool_name](**arguments)
        except Exception as e:
            return json.dumps({"status": "EXECUTION_ERROR", "error": str(e)}, ensure_ascii=False)
    return json.dumps({"status": "UNKNOWN_TOOL", "error": f"Tool '{tool_name}' không tồn tại!"}, ensure_ascii=False)
