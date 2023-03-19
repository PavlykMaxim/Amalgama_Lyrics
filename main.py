from bs4 import BeautifulSoup
import requests
import os

url_name = ''
song_name = ''


def author_first_letter(author):
    first_letter = author[0]
    return first_letter


def author_url_parser(author):
    global url_name
    author_name_list = author.split()
    if len(author_name_list) == 1:
        return author
    elif len(author_name_list) == 0:
        return 'Нужно обязательно указать автора!'
    else:
        for i in author_name_list:
            url_name = url_name + i + "_"
        return url_name[:len(url_name) - 1]


def song_name_parser(song):
    global song_name
    song_name_list = song.split()
    if len(song_name_list) == 1:
        return song
    elif len(song_name_list) == 0:
        return 'Нужно обязательно указать название песни!'
    else:
        for i in song_name_list:
            song_name = song_name + i + '_'
        return song_name[:len(song_name) - 1]


author_user_request = str(input('Введите название группы/исполнителя:\n').lower())
song_user_request = str(input('Введите название песни:\n').lower())

first_letter = author_first_letter(author_user_request)
author_url_name = author_url_parser(author_user_request)
song_url_name = song_name_parser(song_user_request)


url = f'https://www.amalgama-lab.com/songs/{first_letter}/{author_url_name}/{song_url_name}.html'

response = requests.get(url=url)
html = response.text
soup = BeautifulSoup(html, 'html.parser')

title = soup.find('title').text
if title == 'Документ не найден! 404 Ошибка!':
    print(f'Страница не найдена! Проверьте, правильно ли вы ввели имя исполнителя и название песни!\n'
          f'Автор - {author_url_name}\nНазвание песни - {song_url_name}')
    exit()

os.mkdir(f'Texts/{author_url_name}-{song_url_name}')
big_container = soup.find('div', id='click_area').select('div', class_='string_container')


# # # ОРИГИНАЛ # # #
temp_lyrics_list = []
for container in big_container:
    divs = container.find('div', class_='original')
    if divs is None:
        pass
    else:
        temp_lyrics_list.append(divs)

lyrics_list = []
for i in temp_lyrics_list[:len(temp_lyrics_list) - 1]:
    lyric = i.getText().replace('\n', '')
    lyrics_list.append(lyric)

with open(f'Texts/{author_url_name}-{song_url_name}/{song_url_name}_original.txt', 'w', encoding='utf-8') as file:
    for i in lyrics_list:
        file.write(i + '\n')

print(f"Текст песни {author_url_name}-{song_url_name}_original.txt создан")


# # # ПЕРЕВОД # # #
temp_lyrics_list = []
for container in big_container:
    divs = container.find('div', class_='translate')
    if divs is None:
        pass
    else:
        temp_lyrics_list.append(divs)

lyrics_list = []
for i in temp_lyrics_list[:len(temp_lyrics_list) - 1]:
    lyric = i.getText().replace('\n', '')
    lyrics_list.append(lyric)

with open(f'Texts/{author_url_name}-{song_url_name}/{song_url_name}_translate.txt', 'w', encoding='utf-8') as file:
    for i in lyrics_list:
        file.write(i + '\n')

print(f"Текст песни {author_url_name}-{song_url_name}_translate.txt создан")
