# -*- coding: utf-8 -*-
from matplotlib import cm, pyplot as plt
from upsetplot import UpSet
import random
import xlwt
import pandas as pd

# глобальная переменная, название файла с датасетом
FILENAME = 'mac_data.xls'
fill = "»"


def generate_xls(headers, data):
    """
    Создаёт XLS файл с датасетом и заданными колонками

    :param headers:
    массив заголовков колон

    :param data:
    двумерный массив данных датасета
    """
    output = xlwt.Workbook()
    sheet = output.add_sheet(FILENAME)
    numerator = 0
    print("Генераций колонн: ", end='')
    for el in headers:
        sheet.write(0, numerator, el)
        numerator += 1
        print(f"{headers.index(el)}/{len(headers)}", end='')
    print("\rГотово!")
    rowiterator = 1
    for mac_type in data:
        print(f"Заполнение данных типа {mac_type}: ")
        for line in data[mac_type]:
            sheet.write(rowiterator, len(headers) - 1, mac_type)
            for i in range(len(headers) - 1):
                sheet.write(rowiterator, i, headers[i] in line)
            print(f"\r{str(data[mac_type].index(line))}/{str(len(data[mac_type]))}", end='')
            rowiterator += 1
        print("\rГотово!")
    try:
        output.save(FILENAME)
        print("Файл датасета успешно создан")
    except FileExistsError:
        print("Файл уже существует. Программа продолжит свою работу используя старый файл")
    except Exception as e:
        print(e)


def make_distinct(data) -> set:
    """
    Создает множество уникальных элементов из словаря, где в качестве значений используется двумерный массив

    :param data:
    словарь с двумерным массивом данных

    :return:
    множество уникальных элементов
    """
    result = set()
    for el in data:
        for el2 in data[el]:
            for el3 in el2:
                result.add(el3)
    return result


def generate_dataset(table, dataset_length=100, bill_len=6) -> list:
    """
    Генерирует датасет по указанным данным и с указанными параметрами

    :param table:
    словарь допустимых данных, где ключ - строка элемент множества,
    а значение - вероятность появление этого элемента в строке датасета

    :param dataset_length:
    количество строк в итоговом датасете

    :param bill_len:
    максимально допустимая длинна одной строки в датасете

    :return:
    массив строк итогового датасета
    """
    result = []
    print("Генераций элемента датасета: ")
    for _ in range(dataset_length):
        bluda = []
        keys = list(table.keys())
        random.shuffle(keys)
        for el in keys:
            probability = table[el] * 10
            if random.randint(0, 11) < probability:
                bluda.append(el)
                if len(bluda) == bill_len:
                    break
        if len(bluda) == 0:
            bluda.append(random.choice(list(table.keys())))
        result.append(bluda)
        print(f"\r{_}/{dataset_length}", end='')
    print("\rГотово!")
    return result


def makedata():
    """
    Создаёт набор датасетов и xls файл с данным набором.

    Генерирует датасеты соответствующие МакДоналдс, МакАвто и МакКафе с заданными вероятностями и размерами чеков
    """
    result = {
        'mac_main': generate_dataset(table={
        "БигМак": 0.8,
        "БигТейсти": 0.5,
        "Чизбургер": 0.4,
        "МакЧикен премьер": 0.3,
        "Гамбургер": 0.2,
        "Нагетсы": 0.7,
        "Картошка": 0.8,
        "Пирожок с вишней": 0.6,
        "Цезарь ролл": 0.3,
        "МакФлурри": 0.4,
        "кофе": 0.7,
        "чай черный": 0.4,
        "чай зеленый": 0.4,
        "прохладительные напитки": 0.8
    }, bill_len=3),
        'mac_avto': generate_dataset(table={
            "БигМак": 0.8,
            "БигТейсти": 0.5,
            "МакЧикен премьер": 0.5,
            "Нагетсы": 0.7,
            "Картошка": 0.8,
            "Цезарь ролл": 0.4,
            "МакФлурри": 0.6,
            "кофе": 0.6,
            "чай черный": 0.5,
            "чай зеленый": 0.5,
            "прохладительные напитки": 0.6
        }, bill_len=3),
        'mac_cafe': generate_dataset(table={
            "Пирожок с вишней": 0.3,
            "Пирожок с яблоком": 0.3,
            "МакФлурри": 0.4,
            "МакФлурри клубничный": 0.4,
            "Макдесерт": 0.4,
            "кофе": 0.7,
            "чай черный": 0.4,
            "чай зеленый": 0.4,
            "молочный коктейль": 0.8
        }, bill_len=3),
    }
    print("Датасет сгенерирован")
    generate_xls(
        list(make_distinct(result)) + ['type'],
        result
    )


def main():
    """
    Функция построения графика.

    :return:
    0 - если выполнение не было прервано
    иначе - код ошибки
    """
    try:
        df = pd.read_excel(FILENAME)
    except Exception as e:
        print("""Возникли проблемы при открытии файла датасета.
Напечатайте details для того чтобы просмотреть подробности.
Или makedata для того чтобы сгенерировать датасет 
        """)
        cmd = input('').lower()
        if cmd == 'details':
            print(e)
        elif cmd == 'makedata':
            makedata()
            main()
        return
    try:
        df = df.set_index(list(df.keys())[:-1])
        upset = UpSet(df,
                      intersection_plot_elements=0)
        upset.add_stacked_bars(by="type", colors=cm.Pastel1,
                               title="Count by type", elements=10)
        upset.plot()
        plt.show()
    except Exception as e:
        print("Возникли проблемы при построении графика.")
        print(e)


if __name__ == '__main__':  # Python entrypoint
    makedata()
    main()
