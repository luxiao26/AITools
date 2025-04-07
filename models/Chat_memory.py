from langchain_community.chat_message_histories import ChatMessageHistory
store = {}
def get_message_history(session_id)->ChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]
