# -*- coding: utf-8 -*-
"""04_data_files_Маширов_Даниил.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1f6GniXKqXtDVnHk4yZRuJ-rzWEwXef_w

# Форматы данных (1)

Материалы:
* Макрушин С.В. "Лекция 4: Форматы данных"
* https://docs.python.org/3/library/json.html
* https://docs.python.org/3/library/pickle.html
* https://www.crummy.com/software/BeautifulSoup/bs4/doc.ru/bs4ru.html
* Уэс Маккини. Python и анализ данных

## Задачи для совместного разбора
"""

import json

"""1. Вывести все адреса электронной почты, содержащиеся в адресной книге `addres-book.json`"""

with open('addres-book.json', 'r', encoding='utf-8') as f:
    items = json.load(f)
    
for item in items:
    print(item['email'])

"""2. Вывести телефоны, содержащиеся в адресной книге `addres-book.json`"""

with open('addres-book.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

for item in items:
    for phone in item['phones']:
        print(phone['phone'])

"""3. По данным из файла `addres-book-q.xml` сформировать список словарей с телефонами каждого из людей. """

from bs4 import BeautifulSoup

with open('addres-book-q.xml') as f:
    soup = BeautifulSoup(f, 'xml')

phonebook = []
for person in soup.find_all("address"):
    phones = [phone.next for phone in person.phones.find_all("phone")]
    name = person.find("name").next
    phonebook.append({name: phones})

for item in phonebook:
    for key, value in item.items():
        print(key + ':', ', '.join(value))

"""## Лабораторная работа №4

### JSON

1.1 Считайте файл `contributors_sample.json`. Воспользовавшись модулем `json`, преобразуйте содержимое файла в соответствующие объекты python. Выведите на экран информацию о первых 3 пользователях.
"""

with open('contributors_sample.json', 'r') as f:
    contributors = json.load(f)

for contributor in contributors[:3]: # первые три пользователя
    print(f"Имя: {contributor['name']}")

"""*1.2* Выведите уникальные почтовые домены, содержащиеся в почтовых адресах людей



"""

with open('contributors_sample.json', 'r') as f:
    contributors = json.load(f)

domains = set() # множество удаляет не уникальные

for contributor in contributors:
    email = contributor['mail']
    if email:
        domain = email.split('@')[1] 
        domains.add(domain)

print("Уникальные домены, содержащиеся в почтовых адресах людей:")
for domain in domains:
    print(domain)

"""1.3 Напишите функцию, которая по `username` ищет человека и выводит информацию о нем. Если пользователь с заданным `username` отсутствует, возбудите исключение `ValueError`"""

with open('contributors_sample.json', 'r') as f:
    contributors = json.load(f)


def find_contributor_by_username(username):
    with open('contributors_sample.json', 'r') as f:
        contributors = json.load(f)

    for contributor in contributors:
        if contributor['username'] == username:
            print(f"Никнейм: {contributor['username']}")
            print(f"Имя: {contributor['name']}")
            print(f"Пол: {contributor['sex']}")
            print(f"Адрес: {contributor['address']}")
            print(f"Email: {contributor['mail']}")
            print(f"Работы: {contributor['jobs']}")
            print(f"ID: {contributor['id']}")
            return
        
    raise ValueError(f"Пользователь с username '{username}' не найден.")

find_contributor_by_username('woodmarissa')
#find_contributor_by_username('Volokolamsk')

"""1.4 Посчитайте, сколько мужчин и женщин присутсвует в этом наборе данных."""

with open('contributors_sample.json', 'r') as f:
    contributors = json.load(f)


male_count = 0
female_count = 0

for contributor in contributors:
    if contributor['sex'] == 'M':
        male_count += 1
    elif contributor['sex'] == 'F':
        female_count += 1

print(f"Количество мужчин: {male_count}")
print(f"Количество женщин: {female_count}")

"""1.5 Создайте `pd.DataFrame` `contributors`, имеющий столбцы `id`, `username` и `sex`."""

import pandas as pd
with open('contributors_sample.json', 'r') as f:
    contributors = json.load(f)

contributors_dict = {'id': [], 'username': [], 'sex': []}

for contributor in contributors:
    contributors_dict['id'].append(contributor['id'])
    contributors_dict['username'].append(contributor['username'])
    contributors_dict['sex'].append(contributor['sex'])

contributors = pd.DataFrame.from_dict(contributors_dict)
contributors

"""1.6 Загрузите данные из файла `recipes_sample.csv` (__ЛР2__) в таблицу `recipes`. Объедините `recipes` с таблицей `contributors` с сохранением строк в том случае, если информация о человеке отсутствует в JSON-файле. Для скольких человек информация отсутствует?

### pickle

2.1 На основе файла `contributors_sample.json` создайте словарь следующего вида: 
```
{
    должность: [список username людей, занимавших эту должность]
}
```
"""

from collections import defaultdict
import json

with open('contributors_sample.json', 'r') as f:
    contributors = json.load(f)

positions = defaultdict(list)

for contributor in contributors:
    for position in contributor['jobs']:
        positions[position].append(contributor['username'])

#print(dict(positions))

for key, value in positions.items():
    print(f"{key}: {value}\n")

from collections import defaultdict
import json

with open('contributors_sample.json', 'r') as f:
    contributors = json.load(f)

positions = defaultdict(list)

for contributor in contributors:
    for position in contributor['jobs']:
        positions[position].append(contributor['username'])

print(dict(positions))

"""2.2 Сохраните результаты в файл `job_people.pickle` и в файл `job_people.json` с использованием форматов pickle и JSON соответственно. Сравните объемы получившихся файлов. При сохранении в JSON укажите аргумент `indent`."""

import pickle

# сохранение в файл
with open('job_people.pickle', 'wb') as f:
    pickle.dump(dict(positions), f)

with open('job_people.json', 'w') as f:
    json.dump(dict(positions), f, indent=4)

"""2.3 Считайте файл `job_people.pickle` и продемонстрируйте, что данные считались корректно. """

with open('job_people.pickle', 'rb') as f:
    job_people = pickle.load(f)

print(job_people)

"""### XML

3.1 По данным файла `steps_sample.xml` сформируйте словарь с шагами по каждому рецепту вида `{id_рецепта: ["шаг1", "шаг2"]}`. Сохраните этот словарь в файл `steps_sample.json`
"""

import json
from bs4 import BeautifulSoup

# Открываем файл с помощью BeautifulSoup
with open('steps_sample.xml', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'xml')

# Извлекаем все элементы recipe из файла
recipes = soup.find_all('recipe')

# Создаем словарь для хранения шагов по каждому рецепту
steps_dict = {}

# Обходим каждый элемент <recipe> и извлекаем его id и шаги
for recipe in recipes:
    recipe_id = recipe.find('id').text
    steps = [step.text for step in recipe.find('steps').find_all('step')]
    steps_dict[recipe_id] = steps

# Сохраняем словарь в файл в формате JSON
with open('steps_sample.json', 'w', encoding='utf-8') as f:
    json.dump(steps_dict, f, ensure_ascii=False, indent=4)

"""3.2 По данным файла `steps_sample.xml` сформируйте словарь следующего вида: `кол-во_шагов_в_рецепте: [список_id_рецептов]`"""

from bs4 import BeautifulSoup


with open("steps_sample.xml", "r") as f:
    xml_data = f.read()

soup = BeautifulSoup(xml_data, "xml")

# Создаем словарь для хранения кол-ва шагов и соответствующих рецептов
steps_count_dict = {}

# Ищем все теги recipe
for recipe in soup.find_all("recipe"):
    # Ищем все теги step внутри текущего recipe
    steps = recipe.find_all("step")
    # Получаем количество шагов
    num_steps = len(steps)
    # Добавляем текущий id в список рецептов для этого количества шагов
    if num_steps in steps_count_dict:
        steps_count_dict[num_steps].append(recipe.id.string)
    else:
        steps_count_dict[num_steps] = [recipe.id.string]

print(steps_count_dict)

for key, value in steps_count_dict.items():
    print(f"{key}: {value}\n")

"""3.3 Получите список рецептов, в этапах выполнения которых есть информация о времени (часы или минуты). Для отбора подходящих рецептов обратите внимание на атрибуты соответствующих тэгов."""

from bs4 import BeautifulSoup

# Загружаем xml-файл и создаем объект BeautifulSoup
with open('steps_sample.xml', 'r') as f:
    xml_data = f.read()
soup = BeautifulSoup(xml_data, 'xml')

# Ищем тэги recipe
recipes = soup.find_all('recipe')

# Создаем список id рецептов, в которых есть информация о времени
recipes_with_time_info = []
for recipe in recipes:
    steps = recipe.steps.find_all('step')
    for step in steps:
        if 'has_minutes' in step.attrs or 'has_hours' in step.attrs:
            recipes_with_time_info.append(recipe.id.string)

# Выводим список id рецептов, в которых есть информация о времени
print(recipes_with_time_info)

"""3.4 Загрузите данные из файла `recipes_sample.csv` (__ЛР2__) в таблицу `recipes`. Для строк, которые содержат пропуски в столбце `n_steps`, заполните этот столбец на основе файла  `steps_sample.xml`. Строки, в которых столбец `n_steps` заполнен, оставьте без изменений.

3.5 Проверьте, содержит ли столбец `n_steps` пропуски. Если нет, то преобразуйте его к целочисленному типу и сохраните результаты в файл `recipes_sample_with_filled_nsteps.csv`
"""

