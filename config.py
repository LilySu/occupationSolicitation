import os

model_name = "text-embedding-ada-002"
index_name = "keyword"

extractedPostingPath = "C:\\Users\\User\\git\\occupationalSolicitation\\yc_jobs\\"

myResumePath = "C:\\Users\\User\\git\\occupationalSolicitation\\my_resumes\\2023-10-27_my_latest_resume.txt"

pineconeKey = os.environ.get("PINECONE_API_KEY")

openAIKey = os.environ.get("OPENAI_API_KEY")

YC_username = os.environ.get("YC_USERNAME")

YC_password = os.environ.get("YC_PASSWORD")

# Set filter parameters individually
demographic = "any"
hasEquity = "any"
hasSalary = "any"
industry = "any"
interviewProcess = "any"
jobType = "any"
layout = "list-compact"
locations = "US" # For testing "US" for United States
remote = "any"
role = "eng"
role_type = "any" # or "ml" for machine learning
sortBy = "created_desc"
tab = "any"
usVisaNotRequired = "any"

filter_params = (
    f"demographic={demographic}&hasEquity={hasEquity}&hasSalary={hasSalary}&"
    f"industry={industry}&interviewProcess={interviewProcess}&jobType={jobType}&"
    f"layout={layout}&locations={locations}&remote={remote}&"
    f"role={role}&role_type={role_type}&sortBy={sortBy}&tab={tab}&usVisaNotRequired={usVisaNotRequired}"
)

chromedriverPath = os.environ.get("CHROMEDRIVER_PATH")