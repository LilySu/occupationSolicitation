import os

chromedriverPath = os.environ.get("CHROMEDRIVER_PATH")

extractedPostingPath = "C:\\Users\\User\\git\\occupationalSolicitation\\yc_jobs\\2023-10-27--yc-job-61198.txt"

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
locations = "IN" # For testing "US" for United States
remote = "yes"
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
