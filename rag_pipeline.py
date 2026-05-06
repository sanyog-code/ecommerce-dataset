import time
from dotenv import load_dotenv
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain

load_dotenv()


def load_pipeline():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.load_local(
        "faiss_walmart_index",
        embeddings,
        allow_dangerous_deserialization=True
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.6,
        max_tokens=2048
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    prompt = PromptTemplate(
        input_variables=["context", "chat_history", "question"],
        template="""
You are an intelligent e-commerce assistant for an online retail store.

Answer customer questions strictly using the provided Walmart product catalog.
You may answer about:
- product features
- prices
- categories
- availability
- comparisons

DO NOT make assumptions or hallucinate.
If the information is NOT present in the dataset, clearly say:
"The requested information is not available in the product catalog."

Context:
{context}

Conversation History:
{chat_history}

Customer Question:
{question}

Answer:
"""
    )

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
        combine_docs_chain_kwargs={"prompt": prompt},
    )

    return chain


def ask_question(chain, question):
    start = time.time()
    result = chain.invoke({"question": question})
    latency = time.time() - start

    return {
        "answer": result["answer"],
        "latency": latency,
        "sources": [doc.metadata for doc in result["source_documents"]],
    }
