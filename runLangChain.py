import os
from langchain.document_loaders import TextLoader
from langchain.llms.openai import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chains import RetrievalQA
import pinecone




FILE_PATH = r'.\text.txt'

pinecone.init(api_key=os.environ.get("PINECONE_KEY"), environment="gcp-starter")
print("Hello VectorStore!")
loader = TextLoader(FILE_PATH)
document = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap = 200)
texts = text_splitter.split_documents(document)
print(len(texts))

embeddings = OpenAIEmbeddings(openai_api_key=os.environ.get("OPENAI_KEY"))
docsearch = Pinecone.from_documents(texts, embeddings, index_name="keyword")

qa = RetrievalQA.from_chain_type(
    llm=OpenAI(openai_api_key=os.environ.get("OPENAI_KEY")), chain_type="stuff", retriever=docsearch.as_retriever(), return_source_documents=True
)
query = "what is pinecone, write me a 15-word answer"
result = qa({"query":query})
print(result)