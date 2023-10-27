import pinecone
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms.openai import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone

from config import extractedPostingPath, openAIKey, pineconeKey

# Initialize Pinecone API with API key and environment
pinecone.init(api_key=pineconeKey, environment="gcp-starter")

# Load text documents from the specified path
loader = TextLoader(extractedPostingPath)
document = loader.load()

# Split text documents into chunks for processing
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(document)

# Print the number of text chunks
print(f"Number of text chunks: {len(texts)}")

# Initialize OpenAI Embeddings
embeddings = OpenAIEmbeddings(openai_api_key=openAIKey)

# Create a Pinecone index from the text chunks
docsearch = Pinecone.from_documents(texts, embeddings, index_name="keyword")

# Initialize a RetrievalQA system for question-answering
qa = RetrievalQA.from_chain_type(
    llm=OpenAI(openai_api_key=openAIKey),
    chain_type="stuff",
    retriever=docsearch.as_retriever(),
    return_source_documents=True,
)

# Define a query for the QA system
query = "What is Pinecone? Please provide a 15-word answer."

# Execute the query and retrieve the result
result = qa({"query": query})

# Print the result of the question-answering query
print(result)
