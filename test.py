from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.base import BaseCallbackHandler
from dotenv import load_dotenv
from queue import Queue
from threading import Thread

load_dotenv()
#queue =  Queue()

class StreamingHandler(BaseCallbackHandler):
    def __init__(self,queue):
        self.queue = queue
    
    def on_llm_new_token(self,token, **kwargs):
        #print(token)
        self.queue.put(token)
    
    def on_llm_end(self, response, **kwargs):
        self.queue.put(None)
    
    def on_llm_error(self, error, **kwargs):
        self.queue.put(None)

## if we set streaming as False our chat.stream method will override this.

chat= ChatOpenAI(streaming=True,) 

prompt = ChatPromptTemplate.from_messages([
        ("human:{content}")
    ]
)

class StreamableChain:
    def stream(self,input):
        # print((self(input)))
        # yield 'hi'
        # yield 'there'
        queue =  Queue()
        handler = StreamingHandler(queue)

        def task():
            self(input,callbacks=[handler])
        
        Thread(target=task).start()

        while True:
            token =  queue.get()
            if token is None:
                break
            yield token

class StreamingChain(StreamableChain, LLMChain):
    pass

chain =  StreamingChain(llm=chat, prompt=prompt)

for output in chain.stream(input={"content":"tell me a joke"}):
    print(output)


# chain = LLMChain(
#     llm=chat,
#     prompt=prompt
# )

# output = chain("tell me a joke")
# print(output)

# # messages = prompt.format_messages(content="tell me a joke")

# # output = chat.stream(messages)

# # for message in chat.stream(messages):
# #     print(message.content)