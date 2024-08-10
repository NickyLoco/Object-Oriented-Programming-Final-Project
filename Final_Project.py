import requests
import matplotlib.pyplot as plt
import time
import datetime

# Extraction Step: Collecting data from NYTimes on the three gaming companies - PlayStation, Xbox, and Nintendo
url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
API_KEY = "YNxP1lsvdmqm86vPiDVUPGpeOYBuwwTn"

years = ["2019", "2020", "2021", "2022", "2023"]
console_names = ["PlayStation", "Xbox", "Nintendo Switch"]
total_years = {game_console: [] for game_console in console_names}

#Time when data collection is initiated
start_time = time.time()

for each_year in years:
    begin_date = each_year + "0101"
    if each_year == "2023":
        end_date = "20231214"
    else:
        end_date = each_year + "1231"

    for game_console in console_names:
        params = {'q': f'body:("{game_console}")', 'api-key': API_KEY, 'begin_date': begin_date, 'end_date': end_date}
        response = requests.get(url, params=params)

        #Error handling for issues connecting to NYTimes API
        try:
            results = response.json()["response"]["meta"]["hits"]
        except KeyError:
            print(f"Error retrieving data for {game_console} in {each_year}")
            print(f"Error Message: {response.content}")
            results = 0

        total_years[game_console].append(results)

        #Request delay based on NYTimes FAQ Suggestion
        time.sleep(12)

#Time when data collection is concluded
end_time = time.time()
#The total time needed for the program
runtime = end_time - start_time

# Calculate result of total appearances for each company
results = {game_console: sum(counts) for game_console, counts in total_years.items()}

# Transformation Step:
fig, ax = plt.subplots(figsize=(10, 6))
categories = list(results.keys())
values = list(results.values())

ax.bar(categories, values, color=['blue', 'green', 'red'])
ax.set_title("Total NYTimes Mentions of Gaming Consoles (2019-2023)")
ax.set_xlabel("Gaming Consoles")
ax.set_ylabel("Total Number of Relevant Articles")

# Loading Step:
plt.savefig('2019_2023_Gaming_Console_Relevancy.png')

# Print program runtime
print(f"Program Start: {datetime.datetime.fromtimestamp(start_time)}")
print(f"Program End: {datetime.datetime.fromtimestamp(end_time)}")
print(f"Total Runtime: {datetime.timedelta(seconds=runtime)}")
