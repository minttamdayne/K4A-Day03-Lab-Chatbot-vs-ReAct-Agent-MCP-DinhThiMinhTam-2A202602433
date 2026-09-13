"""Giao diện Streamlit trực quan cho VinUni Library ReAct Agent."""

import contextlib
import io

import streamlit as st

from app import run_react_agent
from mcp_server import MCPAcademicServer
from providers import get_llm_provider


st.set_page_config(
    page_title="VinUni Library Agent",
    page_icon="📚",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {max-width: 1100px; padding-top: 2rem;}
    [data-testid="stChatMessage"] {border: 1px solid rgba(128,128,128,.18); border-radius: 16px;}
    .tool-pill {display:inline-block; padding:.2rem .55rem; margin:.15rem; border-radius:999px;
                background:#eef2ff; color:#3730a3; font-size:.8rem; font-weight:600;}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def create_services():
    return get_llm_provider(), MCPAcademicServer()


def render_trace(trace: list) -> None:
    """Hiển thị waterfall Thought → Action → Observation → Answer."""
    if not trace:
        return
    with st.expander("🔍 Xem Waterfall Trace", expanded=False):
        for event in trace:
            step = event.get("step", "?")
            if event.get("action_type") == "TOOL_EXECUTION":
                st.markdown(f"**Bước {step} · Tool Call — `{event.get('tool_name')}`**")
                cols = st.columns(2)
                with cols[0]:
                    st.caption("Arguments")
                    st.json(event.get("arguments", {}))
                with cols[1]:
                    st.caption("MCP Observation")
                    st.json(event.get("observation", {}))
                st.caption(f"Độ trễ LLM: {event.get('latency_ms', 0)} ms")
            else:
                st.markdown(f"**Bước {step} · Final Answer**")
                st.caption(event.get("thought", "Đã tổng hợp kết quả."))


provider, mcp_server = create_services()

with st.sidebar:
    st.title("⚙️ Hệ thống")
    st.success(f"LLM: {provider.__class__.__name__}")
    st.info(f"Model: {getattr(provider, 'model_name', 'N/A')}")
    st.caption(f"MCP Server: {mcp_server.server_name}")
    st.markdown("**Tools đang hoạt động**")
    pills = "".join(f'<span class="tool-pill">{tool["name"]}</span>' for tool in mcp_server.list_tools())
    st.markdown(pills, unsafe_allow_html=True)
    st.divider()
    show_raw_log = st.toggle("Hiện log kỹ thuật", value=False)
    if st.button("🗑️ Xóa hội thoại", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.title("📚 VinUni Library ReAct Agent")
st.caption("Trợ lý tra cứu tài liệu, kiểm tra lượt mượn và gia hạn sách qua MCP Server")

with st.expander("💡 Câu hỏi mẫu", expanded=not st.session_state.get("messages")):
    st.markdown(
        """
        - Kiểm tra cuốn **Tôi thấy hoa vàng trên cỏ xanh** còn bản nào và nằm ở đâu?
        - Tôi là **SV202602433**, hãy kiểm tra và gia hạn cuốn **Cho tôi xin một vé về tuổi thơ**.
        - Tôi là **SV20260110**, gia hạn cuốn **Ngày xưa có một chuyện tình** thêm một tuần.
        """
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant":
            render_trace(message.get("trace", []))
            if show_raw_log and message.get("raw_log"):
                with st.expander("Log console"):
                    st.code(message["raw_log"], language="text")

if prompt := st.chat_input("Nhập yêu cầu của bạn..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Agent đang suy luận và gọi MCP tools..."):
            console = io.StringIO()
            with contextlib.redirect_stdout(console):
                trace = run_react_agent(prompt, provider, mcp_server)

        final_events = [event for event in trace if event.get("action_type") == "FINAL_ANSWER"]
        answer = final_events[-1].get("output", "Agent chưa tạo được câu trả lời.") if final_events else "Agent chưa tạo được câu trả lời."
        st.markdown(answer)
        render_trace(trace)
        if show_raw_log:
            with st.expander("Log console"):
                st.code(console.getvalue(), language="text")

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "trace": trace,
        "raw_log": console.getvalue(),
    })
