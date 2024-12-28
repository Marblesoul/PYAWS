import bs4
import requests
from bs4 import BeautifulSoup
from datetime import datetime

url = 'https://habr.com/ru/articles/'
KEYWORDS = ['дизайн', 'фото', 'web', 'python']


class HabrParser:
    def __init__(self, link):
        self.url = link
        self.html = None
        self.links = None

    def get_html(self, link: str = None) -> BeautifulSoup | None:
        if link is None:
            response = requests.get(self.url)
            if response.status_code != 200:
                print(f"Error: {response.status_code}")
                return None
            self.html = bs4.BeautifulSoup(response.text, features='lxml')
            return self.html
        else:
            response = requests.get(link)
            if response.status_code != 200:
                print(f"Error: {response.status_code}")
                return None
            self.html = bs4.BeautifulSoup(response.text, features='lxml')
            return self.html

    def get_articles_links(self) -> list[str]:
        items = self.html.find_all('article', class_='tm-articles-list__item')
        self.links = [f"https://habr.com{item.find('a', class_='tm-title__link').get('href')}" for item in items]
        return self.links

    def check_articles(self) -> None:
        res = []
        for link in self.links:
            try:
                html = self.get_html(link)
                if html:
                    date = html.find('time').get('datetime')
                    normal_date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.000z').strftime('%H:%M:%S %d.%m.%Y')
                    header = html.find('h1', class_='tm-title tm-title_h1').text
                    text = html.find('div', class_='tm-article-body').text
                    for word in KEYWORDS:
                        if link not in [i['Ссылка'] for i in res]: # Проверка на повторение
                            if word.lower() in header.lower() or word in text.lower():
                                res.append({'Дата': normal_date, 'Заголовок': header, 'Ссылка': link})
            except Exception as e:
                print(f'Error: {e}')
        for i in res:
            print(i)
        return


if __name__ == '__main__':
    parser = HabrParser(url)
    parser.get_html()
    parser.get_articles_links()
    parser.check_articles() # Проверям статьи с ключевыми словами и выводим их