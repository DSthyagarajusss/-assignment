import requests
from bs4 import BeautifulSoup


url = "https://techcrunch.com/2024/04/30/sams-clubs-ai-powered-exit-tech-reaches-20-of-stores/"
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('h1').get_text()
    content = soup.find_all('p')
    print(f"Title: {title}\n")
    for paragraph in content:
        print(paragraph.get_text())
else:
    print(f"Failed to retrieve the article. Status code: {response.status_code}")
