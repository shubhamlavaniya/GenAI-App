from langchain.chains import ConversationalRetrievalChain
from app.chat.chains.stremable import StreamableChain
from app.chat.chains.traceble import TraceableChain


class StreamingConversationalRetrievalChain(
    TraceableChain, StreamableChain, ConversationalRetrievalChain
):
    pass