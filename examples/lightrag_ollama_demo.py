import os
import logging
from lightrag import LightRAG, QueryParam
from lightrag.llm import ollama_model_complete, ollama_embedding
from lightrag.utils import EmbeddingFunc

WORKING_DIR = "./dickens"

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)

rag = LightRAG(
    working_dir=WORKING_DIR,
    llm_model_func=ollama_model_complete,
    llm_model_name="qwen2.5:7b",
    llm_model_max_async=4,
    llm_model_max_token_size=32768,
    llm_model_kwargs={"host": "http://localhost:11434", "options": {"num_ctx": 32768}},
    embedding_func=EmbeddingFunc(
        embedding_dim=768,
        max_token_size=8192,
        func=lambda texts: ollama_embedding(
            texts, embed_model="nomic-embed-text", host="http://localhost:11434"
        ),
    ),
)

# with open("./output.txt", "r", encoding="utf-8") as f:
#     x = f.readlines()

# for i in x:
#     rag.insert(i)


with open("./output.txt", "r", encoding="utf-8") as f:
    rag.insert(f.read())

# print(
    # rag.query("What are the low performing subjects and topics", param=QueryParam(mode="naive"))
# )

# Perform local search
print(
    rag.query("list all the low performing areas in Physics elaborately with question numbers", param=QueryParam(mode="hybrid"))
)

# print(f"local\n\n")
# # Perform global search
# print(
#     rag.query("What are the low performing subjects and topics in Physics", param=QueryParam(mode="local"))
# )

# print(f"hybrid\n\n")

# # # Perform hybrid search
# print(
#     rag.query("What are the low performing subjects and topics in Physics", param=QueryParam(mode="hybrid"))
# )
