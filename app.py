import streamlit as st
import google.generativeai as genai

# 페이지 설정
st.set_page_config(
    page_title="👩‍💻 Gemini Chatbot",
    page_icon="🤖",
    layout="centered"
)

# API 키 불러오기
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Streamlit 타이틀
st.title("👩‍💻 Gemini Chatbot")

# 이전 메시지 출력
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 사용자 입력
if prompt := st.chat_input("메시지를 입력하세요"):
    # 사용자 메시지 저장 및 출력
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Gemini에 보낼 전체 메시지 구성
    history = [{"role": m["role"], "parts": [m["content"]]} for m in st.session_state["messages"]]

    try:
        response = model.generate_content(history)
        reply = response.text.strip()

        # 모델 응답 저장 및 출력
        st.session_state["messages"].append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.write(reply)
    except Exception as e:
        error_msg = f"오류 발생: {e}"
        st.session_state["messages"].append({"role": "assistant", "content": error_msg})
        with st.chat_message("assistant"):
            st.write(error_msg)
