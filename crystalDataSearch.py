import os

from astrapy.db import AstraDB
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings

# Astra connection
ASTRA_DB_APPLICATION_TOKEN = os.environ.get("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_API_ENDPOINT= os.environ.get("ASTRA_DB_API_ENDPOINT")

db = AstraDB(
    token=ASTRA_DB_APPLICATION_TOKEN,
    api_endpoint=ASTRA_DB_API_ENDPOINT,
)
col = db.collection("crystal_data")

lapidary_template = """
You are a reiki energy healer and crystal enthusiast, tasked with answering questions about precious stones and
their healing properties from patients and other crystal enthusiasts.
You must answer based only on the provided context, do not make up any fact.
Your answers must provide factual details.
You MUST refuse to answer questions on other topics than crystals, precious stones, and their healing properties
as well as questions whose answer is not found in the provided context.

QUESTION: {question}

YOUR ANSWER:"""

llm = ChatOpenAI()
embeddings = OpenAIEmbeddings() #1536

lapidary_prompt = ChatPromptTemplate.from_template(lapidary_template)
#vectorstore = Cassandra(embedding=embeddings, table_name=TABLE_NAME, session=None, keyspace=None)
#retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

chain = (
    #{"context": retriever, "question": RunnablePassthrough()}
    {"question": RunnablePassthrough()}
    | lapidary_prompt
    | llm
    | StrOutputParser()
)

user_input = "which crystals will help with anxiety?"
print(f"\n{user_input}\n")

while user_input != "exit":
    text_emb = embeddings.embed_query(user_input)
    results = col.vector_find(text_emb, limit=3, fields={"text", "$vector"})

    for result in results:
        print(f"{result['text']}\n")

    user_input = input("\nNext search? ")
    print("\n")
