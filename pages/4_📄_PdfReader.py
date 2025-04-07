import streamlit as st
import os
import tempfile

from codes.Pdf_reader import generate_script

# # 设置页面标题和图标
# st.set_page_config(
#     page_title="智能PDF阅读助手",
#     page_icon="📖",
#     layout="centered"
# )

# 页面标题和说明
st.title("📖 智能PDF阅读助手")
st.markdown("""
欢迎使用智能PDF阅读助手！上传您的PDF文档并开始提问吧！
- 支持多轮对话问答
- 自动维护会话历史
- 支持文档内容溯源
""")

# 初始化session状态
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 侧边栏配置
with st.sidebar:
    st.header("配置参数")
    api_key = st.text_input("DeepSeek API密钥", type="password")
    st.markdown("[获取DeepSeek API密钥](https://platform.deepseek.com/usage)")
    session_id = st.text_input("会话ID（输入新ID开始新会话）", "default")

# 文件上传区域
uploaded_file = st.file_uploader("上传PDF文档", type=["pdf"])

# 处理文件上传
file_path = None
if uploaded_file:
    # 创建临时文件
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        file_path = tmp_file.name

# 显示聊天历史
for entry in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(entry["question"])
    with st.chat_message("assistant"):
        st.markdown(entry["answer"])

# 问题输入框
question = st.chat_input("请输入您的问题")

if question:
    # 输入验证
    if not api_key:
        st.error("请先输入API密钥")
        st.stop()
    if not uploaded_file:
        st.error("请先上传PDF文件")
        st.stop()

    # 显示用户问题
    with st.chat_message("user"):
        st.markdown(question)

    try:
        # 调用后端函数
        response = generate_script(
            api_key=api_key,
            files=file_path,
            session_id=session_id,
            question=question
        )

        # 显示回答
        with st.chat_message("assistant"):
            st.markdown(response)

        # 保存到历史记录
        st.session_state.chat_history.append({
            "question": question,
            "answer": response
        })

    except Exception as e:
        st.error(f"发生错误：{str(e)}")

    finally:
        # 清理临时文件
        if file_path and os.path.exists(file_path):
            os.remove(file_path)

# 侧边栏说明
with st.sidebar:
    st.markdown("""
**使用说明：**
1. 输入有效的DeepSeek API密钥
2. 上传PDF文档（小于200MB）
3. 输入或生成新的会话ID开始新对话
4. 在下方输入问题开始问答

**功能特点：**
- 支持上下文关联问答
- 自动维护对话历史
- 答案包含来源标注
- 支持多轮对话
""")