import os

chromedriverPath = os.environ.get("CHROMEDRIVER_PATH")

YC_username = os.environ.get("YC_USERNAME")

YC_password = os.environ.get("YC_PASSWORD")

# Set filter parameters individually
demographic = 'any'
hasEquity = 'any'
hasSalary = 'any'
industry = 'any'
interviewProcess = 'any'
jobType = 'any'
layout = 'list-compact'
locations = 'US'
remote = 'yes'
role = 'eng'
role_type = 'ml'
sortBy = 'created_desc'
tab = 'any'
usVisaNotRequired = 'any'

filter_params = (
    f'demographic={demographic}&hasEquity={hasEquity}&hasSalary={hasSalary}&'
    f'industry={industry}&interviewProcess={interviewProcess}&jobType={jobType}&'
    f'layout={layout}&locations={locations}&remote={remote}&'
    f'role={role}&role_type={role_type}&sortBy={sortBy}&tab={tab}&usVisaNotRequired={usVisaNotRequired}'
)
