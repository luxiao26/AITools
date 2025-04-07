# 1、获取用户密钥，用户对话
# 2、保留用户历史消息（外部传入）
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_deepseek import ChatDeepSeek
from models.Chat_memory import get_message_history
import os
def get_chat_response(prompt,chat_type,session_id,api_key):
    model = ChatDeepSeek(model = "deepseek-chat",api_key= api_key)
    chat_prompt = ChatPromptTemplate.from_messages(
        [
            ("system","你是一个专精于{chat_type}的人工智能助手，请注意保持你的专业性，输出内容严格与用户输入内容相关，确保回复准确易懂"),
            MessagesPlaceholder(variable_name="memory"),
            ("human","{prompt}")
        ]
    )
    chain = chat_prompt|model
    # 聊天记录管理
    memory_chain = RunnableWithMessageHistory(
        chain,
        get_message_history,
        input_messages_key="prompt",
        history_messages_key="memory",
    )
    response = memory_chain.invoke(
        {"chat_type":chat_type,"prompt":prompt},
        config={"configurable":{"session_id":session_id}}
    )
    # 流式传输
    # response = memory_chain.stream(
    #     {"chat_type":chat_type,"prompt":prompt},
    #     config={"configurable":{"session_id":session_id}}
    # )
    return response


# a = get_chat_response("正弦定理是什么", "数学", "1001", os.getenv("DEEPSEEK_API_KEY"))
# b = get_chat_response("那余弦定理呢", "数学", "1001", os.getenv("DEEPSEEK_API_KEY"))
# c = get_chat_response("把他们两个合起来说一遍", "数学", "1001", os.getenv("DEEPSEEK_API_KEY"))

# history = get_message_history("1001")
# # print(history)
# for msg in history.messages:
#     print(msg.content)
# for msg in a:
#     print(msg.content,end="|")
# print(f"b:{b}")
# print(f"c:{c}")