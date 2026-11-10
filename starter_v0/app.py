"""Streamlit UI; launch from starter_v0 with streamlit run app.py."""
import streamlit as st

from chat import create_session
from chat_runtime import safe_error

st.set_page_config(page_title="AI Research Briefing", page_icon="📚", layout="wide")
st.title("AI Research Briefing")
st.caption("Tìm nguồn · Đọc nghiên cứu · Xuất bản tin · Gửi Telegram sau xác nhận")

with st.sidebar:
    st.header("Không gian nghiên cứu")
    st.markdown("Tìm tin và paper về AI, đọc nguồn cụ thể, rồi xuất kết quả có dẫn nguồn.")
    st.markdown("**Thử hỏi**\n\n- Tìm 3 paper về đánh giá AI agent.\n- Xuất danh sách vừa tìm thành CSV.\n- Gửi file đó tới Telegram của nhóm.")
    if st.button("Bắt đầu phiên mới", use_container_width=True):
        st.session_state.pop("research_session", None)
    st.caption("arXiv có thể trả preprint chưa qua phản biện. Kiểm tra nguồn trước khi sử dụng.")

if "research_session" not in st.session_state:
    try:
        st.session_state.research_session = create_session()
        st.session_state.research_session.transcript["input_mode"] = "interactive_web"
    except Exception as exc:
        st.error(safe_error(exc))
        st.stop()
session = st.session_state.research_session
st.sidebar.caption(f"Model: {session.model}")
st.sidebar.caption(f"Version: {session.transcript.get('version', 'test')}")

chat_col, files_col = st.columns([3, 2])
action = None
with chat_col:
    for turn in session.transcript["turns"]:
        with st.chat_message("user"):
            st.write(turn["user"])
        with st.chat_message("assistant"):
            st.markdown(turn["assistant_text"])
            if turn["status"] in ("provider_error", "tool_error", "max_tool_rounds", "stopped"):
                st.error(turn.get("error", turn["status"]))
            for event in turn["tool_events"]:
                result = event.get("result", {})
                if result.get("error"):
                    st.error(f"{event['tool']}: {result.get('message', result['error'])}")
            if turn["tool_events"]:
                with st.expander("Tool và kết quả"):
                    st.json(turn["tool_events"])
    if session.pending:
        st.info("Đang chờ xác nhận. Đổi yêu cầu sẽ hủy xác nhận hiện tại.")
        yes, no = st.columns(2)
        if yes.button("Xác nhận gửi", type="primary", use_container_width=True):
            action = "Xác nhận gửi"
        if no.button("Hủy gửi", use_container_width=True):
            action = "Hủy gửi"

with files_col:
    st.subheader("Tài liệu của phiên")
    if not session.artifacts.artifacts:
        st.caption("Yêu cầu xuất Markdown hoặc CSV để tạo file.")
    for aid, artifact in session.artifacts.artifacts.items():
        with st.container(border=True):
            st.markdown(f"**{artifact['filename']}** · {artifact['item_count']} nguồn")
            with st.expander("Xem trước"):
                st.code(artifact["content"], language="csv" if artifact["filename"].endswith("csv") else "markdown")
            st.download_button("Tải file", data=artifact["content"].encode("utf-8"),
                               file_name=artifact["filename"], mime=artifact["mime_type"],
                               key=f"download_{aid}", on_click="ignore")
            sent = aid in session.artifacts.sent
            if st.button("Đã gửi / đã thử gửi" if sent else "Gửi file tới Telegram", key=f"send_{aid}", disabled=sent):
                action = f"Gửi file có artifact_id={aid} tới Telegram nhóm. Hãy chuẩn bị bước xác nhận."
    if session.sources:
        st.subheader("Nguồn gần nhất")
        for item in session.sources:
            if item.get("url"):
                st.link_button(item.get("title") or item["url"], item["url"])
    if session.transcript["turns"]:
        st.caption(f"Transcript: {session.path.name if session.path else 'test session'}")

prompt = st.chat_input("Bạn muốn tìm hiểu chủ đề nào?")
if action or prompt:
    with st.spinner("Đang xử lý yêu cầu…"):
        session.turn(action or prompt)
    st.rerun()
