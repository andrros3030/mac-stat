from supervenn import supervenn
# from matplotlib_venn import venn2, venn2_circles, venn2_unweighted
# from matplotlib_venn import venn3, venn3_circles
from matplotlib import pyplot as plt
import random


def generate_dataset(filename, table, dataset_length=100, bill_len=6):
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
        file.write(str(bluda) + '\n')
    file.close()


def makedata():
    name1 = 'mac_main.txt'
    name2 = 'mac_avto.txt'
    name3 = 'mac_cafe.txt'
    generate_dataset(name1, table={
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
    generate_dataset(name2, table={
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
    generate_dataset(name3, table={
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
    return [name1, name2, name3]


def get_data():
    return [{1, 2, 3, 4}, {3, 4, 5}, {1, 6, 7, 8}]


def main():
    sets = get_data()
    labels = ['alice', 'bob', 'third party']
    supervenn(sets, labels)
    plt.show()


if __name__ == '__main__':
    makedata()
    # main()
