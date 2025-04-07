# pdf阅读器
# 阅读并回答用户的提问
# 传入apikey，文件，问题
import os

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import ZhipuAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_deepseek import ChatDeepSeek
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models.Pdf_memory import get_memory


def generate_script(api_key,files,session_id,question):
    model = ChatDeepSeek(model = "deepseek-chat",api_key= api_key)
    # 加载数据
    loader = PyPDFLoader(files)
    # 获取文件的list内容
    docs = loader.load()
    # 切割文本
    text_split = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )
    text = text_split.split_documents(docs)
    print(text)
    # 将切分好的文件存储
    vector_store = Chroma.from_documents(text,embedding=ZhipuAIEmbeddings(model = "embedding-3"))
    # 创建检索器
    retriever = vector_store.as_retriever()
    # 提示词
    prompt = ChatPromptTemplate.from_messages(
        ["system","""
【角色定义】
你是一名专业的文档解析专家，具备高效的信息提炼能力和精准的问答处理技术。
根据提供的上下文: {context} /n/n 回答问题: {input}"
执行多维度分析：
√ 关键概念提取（实体识别+术语标注）
√ 逻辑结构映射（章节关系图生成）
√ 信息密度评估（核心段落标定）
【问答模式规范】
进入交互式问答时遵守：
答案溯源：标注引用位置（章节/页码）
置信提示：对模糊信息添加可靠性评级（★-★★★★★）
关联拓展：智能推荐相关延伸问题（3个备选提问建议）
边界声明：对文档未覆盖领域明确说明知识局限
请保证回答的简介，回答的内容不超过三句话""",
         MessagesPlaceholder("history")
         ]
    )
    # 用stuff（填充）的方式创建链
    chain = create_stuff_documents_chain(model,prompt)
    retriever_history_temp = ChatPromptTemplate.from_messages(
        [
            ("system",
             "根据聊天历史记录以及最新的用户问题，引用上下文内容来得到可以被理解一个独立的问题，如果没有问题，请直接返回聊天记录"),
            MessagesPlaceholder("history"),
            ("human", "{input}")
        ]
    )
    # 由于历史记录和检索器都需要上下文chain，所以需要一个子链存储历史记录
    # 创建子链
    history_chain = create_history_aware_retriever(model,retriever,retriever_history_temp)
    # 创建父链:把理解上下文的链和存储记忆和数据的链组合起来
    over_chain = create_retrieval_chain(history_chain,chain)
    # 创建一个带会话历史记录的runnable
    with_message_history = RunnableWithMessageHistory(
        over_chain,
        get_session_history=get_memory,
        input_messages_key="input",
        history_messages_key="history",
        # 输出消息的键
        output_messages_key="answer",
    )
    # 流式传输
    response = with_message_history.invoke(
        {"input":question},
        config = {"configurable":{"session_id":session_id}}
    )
    return response["answer"]
