import streamlit as st
from codes.VideoScript import generate_script
# 添加标题
st.title("视频脚本生成器")
# 添加侧边栏
with st.sidebar:
    # 文字输入
    deepseek_api = st.text_input("请输入deepseek API密钥：",type="password")
    # 添加markdown内容
    st.markdown("[获取DeepSeek API密钥](https://platform.deepseek.com/usage)")
subject = st.text_input("请输入视频的主题")
# 数字输入
video_length = st.number_input("请输入视频的大致时常（单位：分钟）",min_value=0.1,step=0.1)
# 拖拽输入
creativity = st.slider("请输入视频脚本的创造力（数字小说明更严谨，数字大说明更多样）",min_value=0.0,max_value=1.0,value=0.2,step=0.1)
# 按钮(返回布尔值)
submit = st.button("生成脚本")
if submit and not deepseek_api:
    # 提示信息
    st.info("请输入deepseek的API密钥")
    # 终止函数
    st.stop()
if submit and not subject:
    st.info("请输入文本主题")
    st.stop()
if submit and not video_length>=0.1:
    st.info("视频时长太短了！")
    st.stop()
if submit:
    # 加载效果
    with st.spinner(("AI正在思考中，请稍后...")):
        search_result,title,script = generate_script(subject,video_length,creativity,deepseek_api)
    # 成功运行
    st.success("视频脚本已生成！")
    # 副标题
    st.subheader("标题：")
    st.write(title)
    st.subheader("视频脚本：")
    st.write(script)
    # 折叠展开组件
    with st.expander("维基百科搜索结果："):
        st.write(search_result)

