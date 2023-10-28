import pinecone
from langchain.chains import RetrievalQA, LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.indexes import vectorstore
from langchain.llms.openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import retriever
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.schema.runnable import RunnablePassthrough

from config import extractedPostingPath, myResumePath, openAIKey, pineconeKey
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema.document import Document

from langchain.chat_models import ChatOpenAI

# Function to combine the content of two text files into one string
# Function to combine the content of two text files into one and save it in a folder
def combine_text_files_and_save(file1, file2, output_folder, output_file):
    try:
        # Open and read the contents of the first file
        with open(file1, 'r') as f1:
            content1 = f1.read()

        # Open and read the contents of the second file
        with open(file2, 'r') as f2:
            content2 = f2.read()

        # Combine the contents into one string
        combined_text = content1 + content2

        # Create the output folder if it doesn't exist
        import os
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Define the path for the output file
        output_path = os.path.join(output_folder, output_file)

        # Save the combined text to the output file
        with open(output_path, 'w') as output_file:
            output_file.write(combined_text)

        return output_path
    except FileNotFoundError:
        return "One or both files not found."


# Provide the file paths for the two text files
output_folder = 'resume_vs_job'
output_file = 'combined_file.txt'

file1_path = extractedPostingPath
file2_path = myResumePath

output_path = combine_text_files_and_save(file1_path, file2_path, output_folder, output_file)


# Load docs
loader = TextLoader(r'resume_vs_job/combined_file.txt')
data = loader.load()

# Split text
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=400)
jobtext = text_splitter.split_documents(data)

model_name = 'text-embedding-ada-002'
index_name = "keyword"

# Initialize OpenAI Embeddings
embeddings = OpenAIEmbeddings()

# # Initialize Pinecone API with API key and environment
pinecone.init(api_key=pineconeKey, environment="gcp-starter")

# vectorstore = Pinecone.from_documents(documents=all_splits, embedding=OpenAIEmbeddings(), index_name="keyword")

embed = OpenAIEmbeddings(
    model=model_name,
    openai_api_key=openAIKey
)

# switch back to normal index for langchain
index = pinecone.Index(index_name)

# First, check if our index already exists. If it doesn't, we create it
if index_name not in pinecone.list_indexes():
    # we create a new index
    pinecone.create_index(
      name=index_name,
      metric='cosine',
      dimension=1536
)

# The OpenAI embedding model `text-embedding-ada-002 uses 1536 dimensions`
docsearch = Pinecone.from_documents(jobtext, embeddings, index_name=index_name)

# docsearch = Pinecone(index, embeddings.embed_query, "text")

# docsearch.add_texts(my_resume_text)

# query = "What is Fleek's job listing number?"
query = "What is my phone number on my resume?"

docs = docsearch.similarity_search(query)

print(docs[0].page_content)





# # Open the text file in read mode
# with open(extractedPostingPath, 'r', encoding='utf-8') as file:
#     # Read the entire content of the file into a string
#     job_description = file.read()

# text_field = "text"
#
# from langchain.vectorstores import Pinecone
# vectorstore = Pinecone(
#     index, embed.embed_query, text_field
# )
# query = " which of my qualifications match that of the job position?"

# # Open the text file in read mode
# with open(myResumePath, 'r', encoding='utf-8') as file:
#     # Read the entire content of the file into a string
#     query = file.read()



# query = "What is Fleek and what is the job title that Fleek is hiring for"

# vectorstore.similarity_search(
#     query,  # our search query
#     k=3  # return 3 most relevant docs
# )
#
# # completion llm
# llm = ChatOpenAI(
#     openai_api_key=openAIKey,
#     model_name='gpt-3.5-turbo',
#     temperature=0.0
# )

# # Open the text file in read mode
# with open(extractedPostingPath, 'r', encoding='utf-8') as file:
#     # Read the entire content of the file into a string
#     job_description = file.read()

# prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
#
# {context}
#
# Question: Based on the following resume {question}, which of my qualifications match that of the job position?
# """


# prompt_template ="""
#       given the job_description {job_description},  I want you to compare against my_resume_data {my_resume_data}:
#             1. Start a conversation in a friendly, personable, but highly professional tone with the team at this startup.
#             Do not include fluff such as "I hope this message finds you well. I recently came across the job description"
#             Suppose you saw this job listing through the Y-combinator job board and you decided to apply right away.
#             Make the response concise and to the point, showing efficiency. Write at least 51 characters but less than 200 characters.
#             2. Write less than 200 characters. Share something based on the qualifications of my_resume_data {my_resume_data}
#             on how I can uniquely move this company forward, and why I am qualified for this role.
#             Vouch for how my_resume_data {my_resume_data} makes me seem like an ideal candidate for them by selling them on my strengths.
#             3. Write about why I am uniquely qualified for this role and why I would be the best fit for their team.
#             Extract out any related experience and paint a verbal picture of why I would be the right candidate.
#             4. Do not end with anything generic like "Thank you for considering my application. I am excited about the opportunity to join your team
#              and contribute to building a video-first native experience for wholesale." Instead, end abruptly saying
#              something like "I'd be happy to talk further via email or linkedin." Do not include brackets to fill in later such as [Your Name].
#             5. Do not include any fill in the blanks such as [Your Name]. and do not include brackets to fill in later.
#             Answer in short one-sentence paragraphs like professional copywriting for email marketing campaigns,
#              6. Make the message a bit more personalized based on any company information that has been provided. Show a positive opinion or provide an endearing compliment that is professional.
#             Question: {job_description}
#             Helpful Answer:"""


# prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
#
# {context}
#
# Question: {question}
# Answer in Italian:"""
# PROMPT = PromptTemplate(
#     template=prompt_template, input_variables=["context", "question"]
# )
#
#
#
# PROMPT = PromptTemplate(
#     template=prompt_template, input_variables=["job_description", "my_resume_data"]
# )
#
# chain_type_kwargs = {"prompt": PROMPT}
#
# qa = RetrievalQA.from_chain_type(
#     llm=llm,
#     chain_type="stuff",
#     retriever=vectorstore.as_retriever(),
#     chain_type_kwargs=chain_type_kwargs
# )
#
# result = qa.run(query)
#
# print(result)



# configure our chat model and authenticate
# llm = ChatOpenAI(
#     temperature=0,
#     model_name="gpt-3.5-turbo",
#     openai_api_key=openAIKey,
# )
#
# #
# # Initialize Pinecone API with API key and environment
# pinecone.init(api_key=pineconeKey, environment="gcp-starter")
# # Initialize OpenAI Embeddings
# embeddings = OpenAIEmbeddings()
#
#
# # Load Text
# job_desc_loader = TextLoader(extractedPostingPath)
# job_description = job_desc_loader.load()
#
# # Split text
# text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=400)
# jobtext = text_splitter.split_documents(job_description)
# #
# # The OpenAI embedding model `text-embedding-ada-002 uses 1536 dimensions`
# docsearch = Pinecone.from_documents(jobtext, embeddings, index_name="keyword")
#
# question = "What is the job Title?"
# # docs = docsearch.similarity_search(question)
# # print(len(docs))
# # print(docs)
#
# context = "job number is 3507"
#
# template = """Use the following pieces of context to answer the question at the end.
# If you don't know the answer, just say that you don't know, don't try to make up an answer.
# Use three sentences maximum and keep the answer as concise as possible.
# Always say "thanks for asking!" at the end of the answer.
# {context}
# Question: {question}
# Helpful Answer:"""
# rag_prompt = PromptTemplate.from_template(template)
#
# rag_chain = (
#     {"context": retriever, "question": RunnablePassthrough()}
#     | rag_prompt
#     | llm
# )
#
# result = rag_chain.invoke("What is the job number?")
# print(result)

# # Load Text
# my_resume_loader = TextLoader(myResumePath)
# my_resume_data = my_resume_loader.load()
#
# # Split text documents into chunks for processing
# text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=400)
# resumetext = text_splitter.split_documents(my_resume_data)

#
# # our dynamic prompt template
# summary_template ="""
#       given the job_description {job_description},  I want you to compare against my_resume_data {my_resume_data}:
#             1. Start a conversation in a friendly, personable, but highly professional tone with the team at this startup.
#             Do not include fluff such as "I hope this message finds you well. I recently came across the job description"
#             Suppose you saw this job listing through the Y-combinator job board and you decided to apply right away.
#             Make the response concise and to the point, showing efficiency. Write at least 51 characters but less than 200 characters.
#             2. Write less than 200 characters. Share something based on the qualifications of my_resume_data {my_resume_data}
#             on how I can uniquely move this company forward, and why I am qualified for this role.
#             Vouch for how my_resume_data {my_resume_data} makes me seem like an ideal candidate for them by selling them on my strengths.
#             3. Write about why I am uniquely qualified for this role and why I would be the best fit for their team.
#             Extract out any related experience and paint a verbal picture of why I would be the right candidate.
#             4. Do not end with anything generic like "Thank you for considering my application. I am excited about the opportunity to join your team
#              and contribute to building a video-first native experience for wholesale." Instead, end abruptly saying
#              something like "I'd be happy to talk further via email or linkedin." Do not include brackets to fill in later such as [Your Name].
#             5. Do not include any fill in the blanks such as [Your Name]. and do not include brackets to fill in later.
#             Answer in short one-sentence paragraphs like professional copywriting for email marketing campaigns,
#              6. Make the message a bit more personalized based on any company information that has been provided. Show a positive opinion or provide an endearing compliment that is professional.
#             Question: {job_description}
#             Helpful Answer:"""
#
# # indicate the format of our prompt
# # rag_prompt_custom = PromptTemplate(input_variables=["job_description", "my_resume_data"], template=summary_template)
# #
# # chain_type_kwargs = {"prompt": rag_prompt_custom}
# # qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=docsearch.as_retriever())
# #
# # query = "print the context"
# # result = qa.run(query)
# # print(result)
# context = "Task Decomposition is Lily Su"
#
# question = "What are the approaches to Task Decomposition?"
#
# template = """Use the following pieces of context to answer the question at the end.
# If you don't know the answer, just say that you don't know, don't try to make up an answer.
# Use three sentences maximum and keep the answer as concise as possible.
# Always say "thanks for asking!" at the end of the answer.
# {context}
# Question: {question}
# Helpful Answer:"""
# #
# rag_prompt_custom = PromptTemplate.from_template(template)
# rag_chain = (
#     {"context": retriever, "question": RunnablePassthrough()}
#     | rag_prompt_custom
#     | llm
# )
#
# rag_chain.invoke("What is Task Decomposition?")

# chain_type_kwargs = {"prompt": rag_prompt_custom}
# qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=docsearch.as_retriever(), chain_type_kwargs=chain_type_kwargs)


#
# # set up our LangChain chain with our dynamic prompt
# chain = LLMChain(llm=llm, prompt=summary_prompt_template)
#
# # run our chain
# result = chain.run(job_description=job_description, my_resume_data=my_resume_data)
#
#
#
# print(result)

#
# # Initialize Pinecone API with API key and environment
# pinecone.init(api_key=pineconeKey, environment="gcp-starter")
#
# job_desc_loader = TextLoader(extractedPostingPath)
# job_description = job_desc_loader.load()
#
#
# # Split text documents into chunks for processing
# text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=400)
# jobtext = text_splitter.split_documents(job_description)
#
# # Print the number of text chunks
# print(f"Number of job text chunks: {len(jobtext)}")
#
# # Initialize OpenAI Embeddings
# embeddings = OpenAIEmbeddings()
#
# # The OpenAI embedding model `text-embedding-ada-002 uses 1536 dimensions`
# docsearch = Pinecone.from_documents(jobtext, embeddings, index_name="keyword")
#
# # my_resume_loader = TextLoader(myResumePath)
# # my_resume_data = my_resume_loader.load()
# #
# # # Split text documents into chunks for processing
# # text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=400)
# # resumetext = text_splitter.split_documents(my_resume_data)
#
# # Open the text file in read mode
# with open(myResumePath, 'r', encoding='utf-8') as file:
#     # Read the entire content of the file into a string
#     file_content = file.read()
#
# docsearch.add_texts(file_content)
#
# # Print the number of text chunks
# # print(f"Number of resume text chunks: {len(resumetext)}")
#
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
# query = "given the job_description {job_description},  I want you to compare against my_resume_data {my_resume_data}: \
#             1. Start a conversation in a friendly, personable, but highly professional tone with the team at this startup.\
#             Do not include fluff such as I hope this message finds you well. I recently came across the job description\
#             Suppose you saw this job listing through the Y-combinator job board and decided to apply right away. \
#             Make the response concise and to the point, showing efficiency. Write at least 51 characters but less than 200 characters. \
#             2. Write at least 50 characters but less than 200. Share something based on the qualifications of my_resume_data {my_resume_data} \
#             on how I can uniquely move this company forward. \
#             Vouch for how my_resume_data {my_resume_data} makes me seem like an ideal candidate for them by selling them on my strengths. \
#             3. Write about why I am uniquely qualified for this role and why I would be the best fit for their team. \
#             Extract out any related experience and paint a verbal picture of why I would be the right candidate. \
#             4. Do not end with anything like Thank you for considering my application. I am excited about the opportunity to join your team \
#              and contribute to building a video-first native experience for wholesale. Please let me know if there is any additional information  \
#              I can provide or if you would like to discuss my qualifications further.Best regards, [Your Name]. Instead, end abruptly saying \
#              something like I would be happy to talk further via email or linkedin. \
#             5. Do not include any fill in the blanks, do not include a numbered list based on these points in the prompt.  \
#             Answer in short one-sentence paragraphs like professional copywriting for email marketing campaigns, \
#              but do not indent a line in between one paragraph and the next.  \
#              6. Make the message a bit more personalized based on any company information that has been provided showing a positive opinion or provide an endearing compliment that is professional." \
#  \
# # Execute the query and retrieve the result
# result = qa({"query": query})
#
# # Print the result of the question-answering query
# print(result)
