from .pinecone import build_retriver
from functools import partial

retriever_map = {
    "pinecone_1": partial(build_retriver, k=1),
    "pinecone_2": partial(build_retriver, k=2),
    "pinecone_3": partial(build_retriver, k=3)

}