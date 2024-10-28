import requests
from bs4 import BeautifulSoup
import lxml

url = "https://webscraper.io/test-sites"
def get_html(url):
    response = requests.get(url)
    return response.text


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    h2 = soup.find('h2').text
    return h2

def get_more_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    h2 = soup.find_all('h2')
    h2 = soup.find_all('h2')
    h2 = [  i.text for i in h2]

    return h2
def main():
    html = get_html(url)
    data = get_page_data(html)
    more_data = get_more_page_data(html)
    print(data)
    print(more_data)

if __name__ == '__main__':
    main()

