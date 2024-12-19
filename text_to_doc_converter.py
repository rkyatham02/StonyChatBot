import re
from langchain.text_splitter import MarkdownTextSplitter
from langchain.docstore.document import Document

def merge_hyphenated_words(text):
    return re.sub(r"(\w)-\n(\w)", r"\1\2", text)


def fix_newlines(text):
    return re.sub(r"(?<!\n)\n(?!\n)", " ", text)


def remove_multiple_newlines(text):
    return re.sub(r"\n{2,}", "\n", text)


def clean_text(text):
    cleaning_functions = [merge_hyphenated_words, fix_newlines, remove_multiple_newlines]
    for cleaning_function in cleaning_functions:
        text = cleaning_function(text)
    return text


def text_to_docs(text, metadata):
    doc_chunks = []
    text_splitter = MarkdownTextSplitter(chunk_size=2048, chunk_overlap=128)
    chunks = text_splitter.split_text(text)
    for i, chunk in enumerate(chunks):
        doc = Document(page_content=chunk, metadata=metadata)
        doc_chunks.append(doc)
    return doc_chunks


def get_doc_chunks(text, metadata):
    text = clean_text(text)
    doc_chunks = text_to_docs(text, metadata)
    return doc_chunks
