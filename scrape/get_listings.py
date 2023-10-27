from scrape_jobs import load_fields_to_csv
from browse_web import login_to_yc


login_to_yc()

results_list = load_fields_to_csv()

for i in range(1000):
    if results_list.count('NaN') == 10:
        login_to_yc()