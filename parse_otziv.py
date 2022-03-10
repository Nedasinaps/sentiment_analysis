import requests
import bs4
import pandas as pd
from multiprocessing import Pool
from functools import reduce

def parse_page(url):
    parsed_data = []
    try:
        # парсим заданную страницу
        req = requests.get(url)
        print(str(url), req)
        parser = bs4.BeautifulSoup(req.text, 'lxml')
        # ищем ссылки на отдельные модели
        divs_models = parser.findAll('div', attrs={'class':'content'})
        refs = [div.find('a', href=True)['href'] for div in divs_models[:-1]]
    
        # парсим каждую страницу для отдельно взятой модели телефона
        for ref in refs:
            req2 = requests.get('https://otziv-otziv.ru' + ref)
            parser2 = bs4.BeautifulSoup(req2.text, 'lxml')
            # поиск тексты отзывов
            divs_feedback = parser2.findAll('div', attrs={'class':'container-reviews collapsible collapsed'})
            
            # для каждого отзыва ищем комментарий и рейтинг
            for feedback in divs_feedback:
                # из всего отзыва берем только текст после слова 'Комментарий:', если он есть
                comment_ind = feedback.text.find('Комментарий:')
                if comment_ind == -1:
                    continue          # комментария нет
                else:
                    comment = feedback.text[comment_ind+12:].replace('\n', ' ').strip()
                    rating = int(feedback.find('div', attrs={'class':'stars-container'}).attrs['title'][-1])
                    parsed_data.append((comment, rating))
    except requests.exceptions.ConnectionError:
        print('ConnectionError to URL ' + url)
        parsed_data.append(('отстойный телефон', 1))
        
    return parsed_data
                    
                    
if __name__ == '__main__':
    p = Pool(10)
    url_list = ['https://otziv-otziv.ru/katalog/mobilnye-telefony/?page=' + str(n) for n in range(1, 709)]
    map_results = list(p.map(parse_page, url_list))
    reduce_results = reduce(lambda x,y: x + y, map_results)
    train_raw = pd.DataFrame(reduce_results, columns=['data', 'rating'])
    train_raw[['data','rating']].to_csv('train_raw.csv', index = False)
