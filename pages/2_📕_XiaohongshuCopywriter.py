import streamlit as st
from codes.XiaohongshuScript import generate_script
st.title("爆款小红书文案生成器")
with st.sidebar:
    # 文字输入
    deepseek_api = st.text_input("请输入deepseek API密钥：",type="password")
    # 添加markdown内容
    st.markdown("[获取DeepSeek API密钥](https://platform.deepseek.com/usage)")
theme = st.text_input("请输入小红书的主题")
submit = st.button("生成文案")
if submit and not  deepseek_api:
    st.info("请输入DeepSeek的API密钥")
    st.stop()
if submit and not theme:
    st.info("请输生成内容的主题")
    st.stop()
if submit :
    with st.spinner(("AI正在思考中，请稍后...")):
        result = generate_script(theme,deepseek_api)
    # 分割线
    st.divider()
    # 多列布局
    left_column,right_column = st.columns(2)
#     在某一列添加内容
    with left_column:
        for i in range(5):
            st.markdown(f"##### 小红书标题{i+1}")
            st.write(result.titles[i])

    with right_column:
        st.markdown("##### 小红书正文")
        st.write(result.content)

