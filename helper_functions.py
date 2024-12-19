from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from web_crawler import get_data_from_website
from prompt_generation import get_prompt
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import OpenAIEmbeddings
from text_to_doc_converter import get_doc_chunks
import os
import requests

def get_chroma_client():
    embedding_function = OpenAIEmbeddings()
    return Chroma(
        collection_name="website_data",
        embedding_function=embedding_function,
        persist_directory="data/chroma"
    )


def store_docs(url):
    text, metadata = get_data_from_website(url)
    docs = get_doc_chunks(text, metadata)
    vector_store = get_chroma_client()
    vector_store.add_documents(docs)
    vector_store.persist()


def get_response(question, organization_name, organization_info, contact_info):
    chat_history = ""
    chain = make_chain()
    response = chain({
        "question": question,
        "chat_history": chat_history,
        "organization_name": organization_name,
        "organization_info": organization_info,
        "contact_info": contact_info
    })
    return response['answer']


def make_chain():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY is not set. Please set it in your environment.")

    model = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.0,
        verbose=True,
        openai_api_key=openai_api_key
    )

    vector_store = get_chroma_client()
    prompt = get_prompt()
    retriever = vector_store.as_retriever(search_type="mmr", verbose=True)

    chain = ConversationalRetrievalChain.from_llm(
        model,
        retriever=retriever,
        return_source_documents=True,
        combine_docs_chain_kwargs=dict(prompt=prompt),
        verbose=True,
        rephrase_question=False,
    )
    return chain


def is_url_valid(url):
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False