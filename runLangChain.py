import pinecone
from langchain.chains import RetrievalQA, LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms.openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone

from config import extractedPostingPath, openAIKey, pineconeKey








loader = TextLoader(extractedPostingPath)
information = loader.load()

# # The top 5 posts on HackerNews.com on 2023-10-11 pasted in as text
# information = """ 1.
# K3s – Lightweight Kubernetes (k3s.io)
# 55 points by kristianpaul 43 minutes ago | hide | 24 comments
# 2.
# The Deep Link Equating Math Proofs and Computer Programs (quantamagazine.org)
# 60 points by digital55 1 hour ago | hide | 4 comments
# 3.
# Modern Pascal is still in the race (2022) (synopse.info)
# 52 points by open-source-ux 2 hours ago | hide | 24 comments
# 4.
# Vulkan Documentation (vulkan.org)
# 75 points by jlpcsl 3 hours ago | hide | 61 comments
# 5.
# SQL Reserved Words – The Empirical List (modern-sql.com)
# 50 points by mariuz 2 hours ago | hide | 19 comments
# """

# our dynamic prompt template
summary_template = """
      given the information {information}.  I want you to:
            Start a conversation with the team at this startup, 
            write at least 50 characters but less than 200. Share something about the 
            ideal candidate and pose it as you, also write about what you're looking 
            for, or why you are qualified for this role.
  """

# indicate the format of our prompt
summary_prompt_template = PromptTemplate(input_variables=["information"], template=summary_template)

# configure our chat model and authenticate
llm = ChatOpenAI(
    temperature=0,
    model_name="gpt-3.5-turbo",
    openai_api_key=openAIKey,
)

# set up our LangChain chain with our dynamic prompt
chain = LLMChain(llm=llm, prompt=summary_prompt_template)

# run our chain
result = chain.run(information=information)

print(result)











#
#
# # Initialize Pinecone API with API key and environment
# pinecone.init(api_key=pineconeKey, environment="gcp-starter")
#
# # Load text documents from the specified path
# loader = TextLoader(extractedPostingPath)
# document = loader.load()
#
# # Split text documents into chunks for processing
# text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# texts = text_splitter.split_documents(document)
#
# # Print the number of text chunks
# print(f"Number of text chunks: {len(texts)}")
#
# # Initialize OpenAI Embeddings
# embeddings = OpenAIEmbeddings(openai_api_key=openAIKey)
#
# # Create a Pinecone index from the text chunks
# docsearch = Pinecone.from_documents(texts, embeddings, index_name="keyword")
#
# # Initialize a RetrievalQA system for question-answering
# qa = RetrievalQA.from_chain_type(
#     llm=OpenAI(openai_api_key=openAIKey),
#     chain_type="stuff",
#     retriever=docsearch.as_retriever(),
#     return_source_documents=True,
# )
#
# # Define a query for the QA system
# query = "Start a conversation with the team at this startup, write at least 50 characters but less than 250. Share something about you, what you're looking for, or why you are qualified for this role."
#
# # Execute the query and retrieve the result
# result = qa({"query": query})
#
# # Print the result of the question-answering query
# print(result)
