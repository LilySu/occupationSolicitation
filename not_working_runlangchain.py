import os
from langchain.document_loaders import TextLoader
from langchain.llms.openai import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chains import RetrievalQA
import pinecone # client

pinecone.init(api_key=os.environ.get("PINECONE_API_KEY"), environment="gcp-starter")

INDEX_NAME ="keyword"

if __name__ == '__main__':
    print("Hello VectorStore!")
    loader = TextLoader("C:\\Users\\User\\git\\occupationalSolicitation\\text.txt")
    document = loader.load()
    # Finetune for our needs
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100, separator=" ", length_function=len)
    texts = text_splitter.split_documents(document)
    print(len(texts))
    # using ada002 of OpenAI for text embedding
    # LangChain creates a uniform interface to access different embeddings from different embeddors
    embeddings = OpenAIEmbeddings(openai_api_key=os.environ.get("OPENAI_API_KEY"))
    #
    # # Pinecone allows persistent storage
    # from_documents uses OpenAI embeddings API to convert text into vectors
    # stores vectors in Pinecone database in the index
    docsearch = Pinecone.from_documents(document, embeddings, index_name=INDEX_NAME)
    #
    #
    # create a chain
    # context from vectorstore will in included in prompt but not transformed
    # take docsearch transformed to retriever object
    # retrieving relevant context is from vector store with semantic search one opton out of many
    # Usually used with vectorstore
    # Performs augmentation of original prompt with relevant context from vectorstore
    # Similarity search based on euclidean distance
    # Chain translates vectors to chunks to pass to modified prompt
    # new prompt is original plus relevant chunks
    # plugging into prompt = stuffing
    # retriever object takes docsearch as a retriever object
    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(openai_api_key=os.environ.get("OPENAI_API_KEY")), chain_type="stuff", retriever=docsearch.as_retriever()
    )
    query = "what is pinecone, write me a 15-word answer"
    result = qa({"query":query})
    print(result)
    # docres = docsearch.similarity_search(query)
    # print(docres[0].page_content)