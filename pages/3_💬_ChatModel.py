import streamlit as st
from codes.Chat_models import get_chat_response
from models.Chat_memory import get_message_history
import os
import time

# 页面配置
st.set_page_config(
    page_title="AI Chat",
    page_icon="🤖",
    layout="centered"
)

# 初始化session状态
if "messages" not in st.session_state:
    st.session_state.messages = []

# 页面标题
st.title("🤖 AI 智能聊天助手")

# 侧边栏配置
with st.sidebar:
    st.header("设置")
    api_key = st.text_input("DeepSeek API密钥", type="password")
    st.markdown("[获取API密钥](https://platform.deepseek.com/api-keys)")
    session_id = st.text_input("会话ID（输入新ID开始新会话）", "default")

    st.divider()
    if st.button("🔄 清除当前会话历史"):
        if session_id in get_message_history(session_id).store:
            del get_message_history(session_id).store[session_id]
            st.session_state.messages = []
            st.rerun()

# 显示持久化历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 用户输入处理
if prompt := st.chat_input("输入您的问题..."):
    if not api_key:
        st.error("请先在侧边栏输入API密钥")
        st.stop()

    # 添加用户消息（只添加一次）
    if not st.session_state.messages or st.session_state.messages[-1]["content"] != prompt:
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

    # 生成回复
    with st.chat_message("assistant"):
        try:
            # 获取响应对象
            response_obj = get_chat_response(
                prompt=prompt,
                chat_type="通用对话",
                session_id=session_id,
                api_key=api_key
            )
            full_response = response_obj.content

            # 创建专用占位符
            response_placeholder = st.empty()
            current_display = ""

            # 流式输出（不修改session_state）
            for char in full_response:
                current_display += char
                response_placeholder.markdown(current_display + "▌")
                time.sleep(0.02)

            # 最终显示完整内容
            response_placeholder.markdown(current_display)

            # 只添加一次AI回复
            if not any(msg["content"] == current_display for msg in st.session_state.messages):
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": current_display
                })

        except Exception as e:
            error_msg = f"生成失败: {str(e)}"
            st.error(error_msg)
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_msg
            })

# 调试面板
with st.expander("🔧 调试信息"):
    st.write(f"当前会话ID: `{session_id}`")
    st.write("内存历史记录:", [
        (msg.type, msg.content)
        for msg in get_message_history(session_id).messages
    ])
    st.write("界面消息缓存:", st.session_state.messages)