import random
from langchain.chat_models import ChatOpenAI
from app.chat.models import ChatArgs
from app.chat.vector_stores import retriever_map
#from app.chat.vector_stores.pinecone import build_retriver # using retriever map in place of this
#from langchain.chains import ConversationalRetrievalChain
#from app.chat.llms.chatopenai import build_llm
#from app.chat.memories.sql_memory import build_memory
from app.chat.llms import llm_map
from app.chat.memories import memory_map
from app.chat.chains.retrieval import StreamingConversationalRetrievalChain
from app.web.api import get_conversation_components, set_conversation_components
from app.chat.vector_stores.pinecone import build_retriver
from app.web.api import (
    set_conversation_components,
    get_conversation_components
)

from app.chat.score import random_component_by_score
from app.chat.tracing.langfuse import langfuse
from langfuse.model import CreateTrace

def select_components(
        component_type, component_map, chat_args
):
    components = get_conversation_components(
        chat_args.conversation_id
    )
    previous_component = components[component_type]
    if previous_component:
         # this is not the first message of the conversation
        #and I need to use the same component again
        builder = component_map[previous_component]
        return previous_component, builder(chat_args)

    else:
        #this is the first message of the conversation
        # I need to randomly select components
        #random_name = random.choice(list(component_map.keys()))
        random_name = random_component_by_score(component_type,component_map)
        builder = component_map[random_name]
        return random_name, builder(chat_args)

def build_chat(chat_args: ChatArgs):
    """
    :param chat_args: ChatArgs object containing
        conversation_id, pdf_id, metadata, and streaming flag.

    :return: A chain

    Example Usage:

        chain = build_chat(chat_args)
    """

    retriever_name, retriever = select_components(
        "retriever",
        retriever_map,
        chat_args
    )

    llm_name, llm = select_components(
        "llm",
        llm_map,
        chat_args
    )

    memory_name, memory =  select_components(
        "memory",
        memory_map,
        chat_args
    )

    #retriever = build_retriver(chat_args)
    #llm=build_llm(chat_args)
    condense_question_llm = ChatOpenAI(streaming=False)
    #memory = build_memory(chat_args)
    print(f"Running chain with memory: {memory_name}, llm: {llm_name}, retriever: {retriever_name}")
    set_conversation_components(
        chat_args.conversation_id,
        llm=llm_name,
        retriever=retriever_name,
        memory=memory_name
    )

 

    return StreamingConversationalRetrievalChain.from_llm(
        llm=llm,
        memory=memory,
        condense_question_llm= condense_question_llm,
        retriever=retriever,
        metadata=chat_args.metadata
    )
