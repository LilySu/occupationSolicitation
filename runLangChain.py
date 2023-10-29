import os
import re
from operator import itemgetter

import pinecone
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone

from config import extractedPostingPath, myResumePath, openAIKey, pineconeKey, model_name, index_name


# Function to combine the content of two text files into one and save it in a folder
def combine_text_files_and_save(file1, file2, output_folder, output_file):
    try:
        # Open and read the contents of the first file
        with open(file1, 'r', encoding='utf-8', errors='ignore') as f1:
            content1 = f1.read()

        # Open and read the contents of the second file
        with open(file2, 'r', encoding='utf-8', errors='ignore') as f2:
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

def run_langChain():
    # Provide the file paths for the two text files
    output_folder = "resume_vs_job"
    output_file = "combined_file.txt"

    job_listings_folder_path = extractedPostingPath
    file2_path = myResumePath

    # List all files in the folder
    all_files_job_folder = [os.path.join(job_listings_folder_path, f) for f in os.listdir(job_listings_folder_path) if
             os.path.isfile(os.path.join(job_listings_folder_path, f))]

    # Get the most recent file based on modification time
    most_recent_job = max(all_files_job_folder, key=os.path.getmtime)

    output_path = combine_text_files_and_save(
        most_recent_job, file2_path, output_folder, output_file
    )

    # Load docs
    loader = TextLoader(r"resume_vs_job/combined_file.txt")
    data = loader.load()

    # Split text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=400)
    jobtext = text_splitter.split_documents(data)

    # Initialize OpenAI Embeddings
    embeddings = OpenAIEmbeddings()

    # Initialize Pinecone API with API key and environment
    pinecone.init(api_key=pineconeKey, environment="gcp-starter")

    embed = OpenAIEmbeddings(model=model_name, openai_api_key=openAIKey)

    # switch back to normal index for langchain
    index = pinecone.Index(index_name)

    # First, check if our index already exists. If it doesn't, we create it
    if index_name not in pinecone.list_indexes():
        # we create a new index if index is not there
        pinecone.create_index(name=index_name, metric="cosine", dimension=1536)

    # The OpenAI embedding model `text-embedding-ada-002 uses 1536 dimensions`
    docsearch = Pinecone.from_documents(jobtext, embeddings, index_name=index_name)

    retriever = docsearch.as_retriever()

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    template = """
                You are Walter Isaacson writing as an expert-level job coach from themuse.com given the job 
                listing in the context {context} and Lily Su's resume,  I want you to act as Lily Su
                and compare Lily Su's resume in the context {context} with the job listing in the context {context}:
                1. Start a conversation in a friendly, personable, but highly professional tone with the team 
                at this startup. Do not include fluff such as "I hope this message finds you well. I recently 
                came across the job description". Suppose you saw this job listing through the Y-combinator job board 
                and you decided to apply right away. Make the response concise and to the point, showing efficiency. 
                Write at least 150 characters but less than 200 characters.
                2. Do not format as a numbered list. Share something based on the qualifications of the resume 
                context {context} on how I can uniquely move this company forward, how and in what way I can move the 
                company forward and why I am qualified for this role. Vouch for how context {context} makes Lily Su seem 
                like an ideal candidate for them by selling them on my strengths.
                3. Do not end with "Thank you for considering my application. I am excited about 
                the opportunity to join your team and contribute to building a video-first native experience for wholesale." 
                Instead, end abruptly saying something like "I'd be happy to talk further via email or linkedin." 
                4. Answer in short one-sentence paragraphs like professional copywriting for email marketing campaigns,
                6. The message must contain one specific item from the company information of the job listing in the 
                context {context} and make an argument on how Lily Su can best contribute to the company's cause. 
                Show a positive opinion or provide an endearing compliment that is professional.
                7. Share my linkedin, email and phone number listed on the resume.
                Helpful Answer:"""
    rag_prompt_custom = ChatPromptTemplate.from_template(template)

    model = ChatOpenAI()

    rag_chain = (
        {"context": itemgetter("question") | retriever, "question": itemgetter("question")}
        | rag_prompt_custom
        | model
        | StrOutputParser()
    )

    question = {
        "question": "How can you be more specific about why Lily Su would be qualified for this role and why she would \n"
                    "be a great pick that would help move the company forward? \n"
                    "Write at least 150 characters but less than 200 characters. Do not \n"
                    "format as a numbered list. Answer in short one-sentence paragraphs like professional copywriting for \n"
                    "email marketing campaigns that state one point specific to the job description and personal, even \n"
                    "touching."
    }

    custom_applicant_message = str(rag_chain.invoke(question))

    return re.sub(r'\[.*?\]', '', custom_applicant_message)

if __name__ == "__main__":
    print(run_langChain())
    print(str(run_langChain()))