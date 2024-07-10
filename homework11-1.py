# Домашнее задание по теме "Обзор сторонних библиотек Python"
# Если вы решали старую версию задачи, проверка будет производиться по ней.
# Ссылка на старую версию тут.
# Цель: познакомиться с использованием сторонних библиотек в Python и применить их в различных задачах.
#
# Задача:
# Выберите одну или несколько сторонних библиотек Python, например, requests, pandas, numpy, matplotlib,
# pillow.
# После выбора библиотек(-и) изучите документацию к ней(ним), ознакомьтесь с их основными возможностями
# и функциями. К каждой библиотеке дана ссылка на документацию ниже.
# Если вы выбрали:
# requests - запросить данные с сайта и вывести их в консоль.
# pandas - считать данные из файла, выполнить простой анализ данных (на своё усмотрение) и вывести
# результаты в консоль.
# numpy - создать массив чисел, выполнить математические операции с массивом и вывести результаты в консоль.
# matplotlib - визуализировать данные с помощью библиотеки любым удобным для вас инструментом из библиотеки.
# pillow - обработать изображение, например, изменить его размер, применить эффекты и сохранить в другой
# формат.
# В приложении к ссылке на GitHub напишите комментарий о возможностях, которые предоставила вам выбранная
# библиотека и как вы расширили возможности Python с её помощью.

import requests
import pandas
import matplotlib.pyplot as plt

from pprint import pprint

URL = 'https://www.cbr-xml-daily.ru/daily_json.js'

"""
Использование модуля requests
Получить данные о курсах валют с сайта на текущую дату и записать 
полученные данные в переменную r в формате json
"""

r = requests.get(URL)
json_flag = False
if r.ok:
    try:
        r = r.json()
    except requests.exceptions.JSONDecodeError as e:
        print('Содержимое ответа не в формате json', 'От источника был получен следующий ответ',
              r, sep='\n')
    else:
        json_flag = True
pprint(r['Valute'])

"""
Использование модуля pandas
1. Сохранить полученные курсы валют в файле .xlsx
2. Построить график из полученных данных
"""

if json_flag:
    # Формируем список валют для записи в файл
    field_list = ['CharCode', 'NumCode', 'Name', 'Nominal', 'Value']
    val_list = []
    for i in r['Valute']:
        line_ = []
        for j in field_list:
            line_.append(r['Valute'][i][j])
        val_list.append(line_)

    pprint(val_list)

    # Сохраняем полученные данные в файл .xlsx
    df1 = pandas.DataFrame(val_list, columns=field_list)
    with pandas.ExcelWriter(f"val_{r['Date'][0:10]}.xlsx") as writer:
        df1.to_excel(writer, sheet_name=str(r['Date'][0:10]))

"""
Использование модуля matplotlib
Зачитать данные из файла .xlsx, построить график на основе этих данных
"""

if json_flag:
    chart_data = pandas.read_excel(f"val_{r['Date'][0:10]}.xlsx")
    pprint(chart_data)
    fig, ax = plt.subplots()

    ax.set_title('Курсы валют')
    ax.set_xlabel('Коды валют')
    ax.set_ylabel('Курс')
    ax.scatter(chart_data['NumCode'], chart_data['Value'], s=chart_data['Nominal'])

    # chart_data['Value'].plot()
    plt.show()
