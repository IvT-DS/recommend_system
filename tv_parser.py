import os
import pandas as pd
import requests
import bs4
import time
from bs4 import BeautifulSoup
from tqdm import tqdm


# Настройка отображения всех столбцов
pd.set_option('display.max_columns', None)


# Определение столбцов для DataFrame
columns = ['page_url', 'image_url', 'tvshow_title', 'description', 'year', 'genre']

# Имя файла, куда записываем информацию
filename = 'tv_shows.csv'
# Проверка, существует ли файл
if not os.path.isfile(filename):
    # Создание файла с заголовками столбцов и без строк, если он не существует
    pd.DataFrame(columns=columns).to_csv(filename, index=False, encoding='utf-8')

# Создаём список для хранения данных о сериалах
# tv_shows_list = []

# Функция для извлечения информации со страницы сериала
def parse_tv_show(tv_show_page_url, headers={'Content-Type': 'text/html; charset=utf-8'}):
    response = requests.get(tv_show_page_url)
    response.encoding = 'utf-8'  # Устанавливаем кодировку ответа в UTF-8

    # Проверяем, успешно ли был выполнен запрос (код ответа 200)
    if response.status_code == 200:
        # Сохраняем HTML-код страницы в переменную src
        src = response.text     

        soup = BeautifulSoup(src, 'lxml')
        
        # Поиск контейнера заголовка сериала
        tvshow_title_container = soup.find('h1', class_='title__main')
        if tvshow_title_container:
            # Извлечение текста только из текстовых узлов, игнорируя вложенные теги
            tvshow_title = ''.join([t for t in tvshow_title_container.contents if type(t) == bs4.element.NavigableString]).strip()
        else:
            tvshow_title = "None"

        # Поиск описания сериала
        description_element = soup.find('div', class_='HtmlContent')
        if description_element:
            description = description_element.get_text(strip=True, separator=' ') #.strip()
            cleaned_description = description.replace('\xa0', ' ')
        else:
            cleaned_description = "None"

        # Используем лямбда-функцию для поиска по тексту элемента, чтобы найти строку с заголовком "Страна:"
        country_title_element = soup.find('td', class_='info-row__title', text=lambda text: 'Страна:' in text)
        if country_title_element:
            country_value_element = country_title_element.find_next_sibling('td', class_='info-row__value')
            if country_value_element:
                country = country_value_element.find('a').text.strip()
            else:
                country = "None"
        else:
            country = "None"

        # Находим год выхода сериала
        # Находим элемент с классом `info-row__title`, который содержит текст 'Даты выхода:'        
        date_title_element = soup.find('td', class_='info-row__title', text=lambda text: 'Даты выхода: ' in text)
        if date_title_element:
            # Используем .find_next_sibling() для нахождения следующего элемента `td` с классом `info-row__value`,
            # который является собственно значением дат
            date_value_element = date_title_element.find_next_sibling('td', class_='info-row__value')
            if date_value_element:
                # Извлекаем текст из найденного элемента и обрабатываем его для получения года
                date_text = date_value_element.text.strip()

                # Получаем год начала показа сериала
                start_date = date_text.split(' — ')[0]  # Разделяем текст по тире и берем первую часть
                year = start_date.split('.')[-1]  # Разделяем дату начала по точке и берем последнюю часть (год)
            else:
                year = "None"
        else:
            year = "None"
        

        # Находим жанры сериала
        # Находим элемент с классом `info-row__title`, который содержит текст 'Жанры:'
        genre_title_element = soup.find('td', class_='info-row__title', text=lambda text: 'Жанры:' in text)
        if genre_title_element:
            # Используем .find_next_sibling() для нахождения следующего элемента `td`, 
            # который является собственно списком жанров
            genre_value_element = genre_title_element.find_next_sibling('td')
            if genre_value_element:
                # Извлекаем все ссылки внутри этого элемента, каждая из которых соответствует жанру
                genre_links = genre_value_element.find_all('a')

                # Собираем текст каждой ссылки (название жанра) в список
                genres = [link.text for link in genre_links]

                # Объединяем список жанров в строку, разделенную запятыми
                genres_str = ', '.join(genres)
            else:
                genres_str = "None"
        else:
            genres_str = "None"
        
        # Вытягиваем картинку сериала
        image_element = soup.find('div', class_='PicturePoster-picture')
        if image_element:
            img_tag = image_element.find('img')
            if img_tag and 'src' in img_tag.attrs:
                image_url = img_tag['src']
            else:
                image_url = "None"
        else:
            image_url = "None"
        
        return {
            'title': tvshow_title, 
            'description': cleaned_description,
            'country': country,
            'year': year,          
            'genres': genres_str,
            'show_url': tv_show_page_url, 
            'image_url': image_url,  
            }    
    else:
        # В случае ошибки выводим сообщение с кодом ошибки
        print("Ошибка загрузки страницы", response.status_code)

# Цикл по страницам сайта
for page in tqdm(range(1, 111), desc="Обработка страниц"): # 1413 последняя страница
    url = f"https://myshows.me/search/all/?page={page}"
    response = requests.get(url, headers={'Content-Type': 'text/html; charset=utf-8'})
    response.encoding = 'utf-8'  # Устанавливаем кодировку ответа в UTF-8

    soup = BeautifulSoup(response.text, 'lxml')

    # Находим ссылки на страницы сериалов
    # Пример, если ссылки находятся в элементах <a class="tv_show_link">, селектор будет 'a.tv_show_link'
    # # Ищем на странице все элементы с классом 'ShowCol-title', которые содержат названия сериалов
    show_descs = soup.findAll(class_ = 'ShowCol-title')
    # # Перебираем найденные элементы в цикле

    # Список для временного хранения данных сериалов с текущей страницы
    tv_shows_page_data = []

    for show_desc in tqdm(show_descs, desc=f"Обработка сериалов на странице {page}"):
        # Составляем полный URL-адрес страницы сериала, добавляя к базовому адресу часть URL из атрибута 'href' ссылки
        tv_show_url = 'https://myshows.me' + show_desc.find('a').get('href')
        # Получаем данные о сериале
        tv_show_data = parse_tv_show(tv_show_url)
        # Добавляем данные в List
        tv_shows_page_data.append(tv_show_data)
        # time.sleep(1)  # Пауза на 1 секунду между обработкой сериалов

    # Преобразование данных страницы в DataFrame и добавление их в файл
    pd.DataFrame(tv_shows_page_data).to_csv(filename, mode='a', header=False, index=False, encoding='utf-8')

    # Пауза в секундах между обработкой страниц
    time.sleep(2)  # Пауза на 1 секунду
    

# data_df = pd.DataFrame(tv_shows_list)

# Сохраняем DataFrame в файл CSV
# data_df.to_csv('tv_shows.csv', index=False)
