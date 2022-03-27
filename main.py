from matplotlib import cm, pyplot as plt
from upsetplot import generate_counts, plot, from_memberships, UpSet
import random
import xlwt
import pandas as pd

name1 = 'mac_main.txt'
name2 = 'mac_avto.txt'
name3 = 'mac_cafe.txt'
FILENAME = 'mac_data.xls'


def generate_xls(headers, data):
    output = xlwt.Workbook()
    sheet = output.add_sheet(FILENAME)
    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'yyyy-mm-dd hh:mm:ss'
    numerator = 0
    for el in headers:
        sheet.write(0, numerator, el)
        numerator += 1
    rowiterator = 1
    for mac_type in data:
        for line in data[mac_type]:
            sheet.write(rowiterator, len(headers)-1, mac_type)
            for i in range(len(headers)-1):
                sheet.write(rowiterator, i, headers[i] in line)
            rowiterator += 1
    output.save(FILENAME)


def make_distinct(data):
    result = set()
    for el in data:
        for el2 in data[el]:
            for el3 in el2:
                result.add(el3)
    return result


def generate_dataset(filename, table, dataset_length=100, bill_len=6):
    result = []
    file = open(filename, 'w')
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
        file.write(str(bluda) + '\n')
    file.close()
    return result


def makedata():
    result = {}
    result[name1] = generate_dataset(name1, table={
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
    }, bill_len=5)
    result[name2] = generate_dataset(name2, table={
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
    }, bill_len=7)
    result[name3] = generate_dataset(name3, table={
        "Пирожок с вишней": 0.3,
        "Пирожок с яблоком": 0.3,
        "МакФлурри": 0.4,
        "МакФлурри клубничный": 0.4,
        "Макдесерт": 0.4,
        "кофе": 0.7,
        "чай черный": 0.4,
        "чай зеленый": 0.4,
        "молочный коктейль": 0.8
    }, bill_len=3)
    generate_xls(
        list(make_distinct(result)) + ['type'],
        result
    )
    return [name1, name2, name3]


def get_data(filenames):
    """
    Открывает датасеты из указанных файлов и возвращает их в читабельном формате - уникальным набором множеств
    и количеством вхождений этих множеств в датасет

    :param filenames:
    массив файлов в которых находятся датасеты

    :return:
    Возвращает набор множеств данных в виде массива по файлам
    """
    result_list = []
    result_counts = []
    data_like_obj = {
        "value": [],
        "type": [],
        "data": []
    }
    for file in filenames:
        for line in open(file, 'r').readlines():
            tmp_result = set(line.replace('\n', '').split(','))
            if tmp_result not in result_list:
                result_list.append(tmp_result)
                result_counts.append(1)
            else:
                result_counts[result_list.index(tmp_result)] += 1
            data_like_obj["value"].append(tmp_result)
            data_like_obj["type"].append(file)
            data_like_obj["data"].append(1)
    return result_list, result_counts, data_like_obj


def main(filenames=None):
    if filenames is not None:
        data, values, data_like_frame = get_data(filenames)
        example = UpSet(from_memberships(data, values), intersection_plot_elements=0, show_counts=True, facecolor='C1')
        example.plot()
        plt.show()
    else:
        df = pd.read_excel(FILENAME)
        # print("dict:", df.__dict__)
        print('index:', list(df.keys()))
        df = df.set_index(list(df.keys())[:-1])
        # eval("df = df.set_index().set_index(df.Pclass == 1, append=True)")
        upset = UpSet(df,
                      intersection_plot_elements=0)  # disable the default bar chart
        upset.add_stacked_bars(by="type", colors=cm.Pastel1,
                               title="Count by type", elements=10)
        upset.plot()
        plt.show()


if __name__ == '__main__':
    # makedata()  # запускать чтобы создать файлы датасетов
    main()  # запускать чтобы рисовалась картиночка
