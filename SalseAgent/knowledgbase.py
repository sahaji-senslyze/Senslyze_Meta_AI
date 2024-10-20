# Set up a knowledge base
import os
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

load_dotenv(dotenv_path='../.env.local')
groq_api_key = os.getenv('GROQ_API_KEY')



model_name = "BAAI/bge-small-en"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": True}
hf = HuggingFaceBgeEmbeddings(
    model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
)

def setup_knowledge_base(product_catalog: str = None):
    """
    Set up the knowledge base from a product catalog text file.
    """
    # Load product catalog
    with open(product_catalog, "r") as f:
        product_catalog = f.read()
    llm=ChatGroq(groq_api_key=groq_api_key,model_name="llama-3.1-70b-versatile")
    # Split the product catalog text into chunks
    text_splitter = CharacterTextSplitter(chunk_size=20, chunk_overlap=5)
    texts = text_splitter.split_text(product_catalog)

    
    # Create the Chroma vector store for document search
    docsearch = Chroma.from_texts(
        texts, embedding=hf, collection_name="product-knowledge-base"
    )

    # Create the retrieval-based QA chain
    knowledge_base = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=docsearch.as_retriever()
    )
    
    return knowledge_base

# # Example usage:
# knowledge_base = setup_knowledge_base("sample_product_catalog.txt")
# response = knowledge_base.run("product in Price: $299?")
# print(response)