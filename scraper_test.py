import requests
from bs4 import BeautifulSoup

url = "https://webscraper.io/test-sites"
def get_html(url):
    response = requests.get(url)
    return response.text


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    h2 = soup.find('h2').text
    return h2

def main():
    html = get_html(url)
    data = get_page_data(html)
    print(data)

if __name__ == '__main__':
    main()

