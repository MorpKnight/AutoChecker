import requests
from bs4 import BeautifulSoup

url = "http://moss.stanford.edu/results/3/1261129696826/"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    high_plagiarism_names = []

    # Loop through the rows of the table and extract data
    for row in table.find_all('tr')[1:]:
        cells = row.find_all('td')
        cell1 = cells[0].find('a')
        cell2 = cells[1].find('a')
        list_name_cell1 = cell1.text.split('/')
        list_name_cell2 = cell2.text.split('/')
        # print(list_name_cell1)
        for name1, name2 in zip(list_name_cell1, list_name_cell2):
            # print last 5 characters of the name
            plagiarisme_checker1 = int(name1[-4:-2])
            plagiarisme_checker2 = int(name2[-4:-2])
            if plagiarisme_checker1 > 85 and plagiarisme_checker2 > 85:
                high_plagiarism_names.append(name1.split("_")[3])
                high_plagiarism_names.append(name2.split("_")[3])
    print(high_plagiarism_names)
else:
    print("Failed to retrieve the HTML content")

