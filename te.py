import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def collect_user_rates(user_login):
    page_num = 1
    data = []

    while True:
        url = f'https://www.kinopoisk.ru/user/{user_login}/votes/list/ord/date/page/{page_num}/'
        
        # Добавляем заголовки для имитации запроса от браузера
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Отправляем запрос с обработкой ошибок
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Проверяем, что запрос успешен
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе страницы {page_num}: {e}")
            break

        # Парсим HTML
        soup = BeautifulSoup(response.text, 'lxml')
        entries = soup.find_all('div', class_='item')

        # Если элементы не найдены, завершаем цикл
        if len(entries) == 0:
            break

        # Извлекаем данные
        for entry in entries:
            nameRus = entry.find('div', class_='nameRus')
            if nameRus:
                film_name = nameRus.find('a').text.strip()
            else:
                film_name = "Название не найдено"

            release_date = entry.find('div', class_='date')
            if release_date:
                release_date = release_date.text.strip()
            else:
                release_date = "Дата не найдена"

            vote = entry.find('div', class_='vote')
            if vote:
                vote = vote.text.strip()
            else:
                vote = "Оценка не найдена"

            data.append({'film_name': film_name, 'release_date': release_date, 'rating': vote})

        # Переходим на следующую страницу
        page_num += 1
        time.sleep(2)  # Добавляем задержку между запросами

    return data

# Пример использования
user_login = '151837781'  # Замените на нужный логин пользователя
user_rates = collect_user_rates(user_login)

# Сохраняем данные в Excel
df = pd.DataFrame(user_rates)
df.to_excel('user_rates.xlsx', index=False)
print(df)
