import csv

import pandas as pd

content_age_category = [
    '0-17', '18-25', '26-35',
    '36-45', '46-50', '51-55',
    '55+',
]

cities = ["A", "B", "C", "D"]
stay_in_current_city_years = ["0", "1", "2", "3", "4+"]


def read_file():
    file = csv.reader(
        open(r"dataset/black-friday/BlackFriday.csv", encoding="utf-8")
    )

    return file


# 去除重复,排序
def get_non_repeat_list(data):
    category = sorted(pd.unique(data).tolist(), key=lambda x: int(x))
    category.insert(0, "All")
    return category


# 获取商品分类
def get_product_category_1(file=read_file()):
    product_category_1 = []
    product_category_2 = []
    product_category_3 = []

    for i in range(0, 19):
        product_category_2.append([])
        product_category_3.append([])

    for row in file:
        if row[8] == "Product_Category_1":
            continue
        if row[8]:
            product_category_1.append(row[8])
            if row[9]:
                product_category_2[int(row[8])].append(row[9])
                if row[10]:
                    product_category_3[int(row[9])].append(row[10])

    for i in range(1, 19):
        product_category_2[i] = get_non_repeat_list(product_category_2[i])
        product_category_3[i] = get_non_repeat_list(product_category_3[i])

    return [get_non_repeat_list(product_category_1), product_category_2, product_category_3]


# 根据商品类别分类
def file_filter(file, product_category_1, product_category_2, product_category_3):
    new_file = []
    for row in file:
        if product_category_1 == "All":
            new_file.append(row)
        elif product_category_1 == row[8]:
            if product_category_2 == "All":
                new_file.append(row)
            elif product_category_2 == row[9]:
                if product_category_3 == "All" or product_category_3 == row[10]:
                    new_file.append(row)

    return new_file


# 获得饼状图所需数据
def get_age_purchase(file):
    content_purchase_list = [0] * len(content_age_category)

    for row in file:
        if row[3] == 'Age':
            continue
        content_purchase_list[content_age_category.index(row[3])] += int(row[11])

    return [content_purchase_list]


# 获得柱状图所需数据
def get_age_sex_purchase(file):
    content_m_purchase_list = [0] * len(content_age_category)
    content_f_purchase_list = [0] * len(content_age_category)

    for row in file:
        if row[3] == 'Age':
            continue
        if row[2] == 'F':
            content_f_purchase_list[content_age_category.index(row[3])] += int(row[11])
        elif row[2] == 'M':
            content_m_purchase_list[content_age_category.index(row[3])] += int(row[11])

    return [content_m_purchase_list, content_f_purchase_list]


# 获得散点图数据
def get_sales_price(file):
    sales = {}
    price = {}
    total = {}
    category = {}
    for row in file:
        if row[1] == "Product_ID":
            continue
        if row[1] in sales:
            sales[row[1]] += 1
            price[row[1]] = (price[row[1]] + int(row[11])) >> 1
            total[row[1]] += int(row[11])
        else:
            sales[row[1]] = 0
            price[row[1]] = int(row[11])
            total[row[1]] = int(row[11])
            category[row[1]] = row[8] + '-' + row[9] + '-' + row[10]

    product_id = []
    product_sales = []
    product_price = []
    product_total = []
    product_category = []

    for key in sales:
        product_id.append(key)
        product_sales.append(sales[key])
        product_price.append(price[key])
        product_total.append(total[key])
        product_category.append(category[key])

    return [product_id, product_sales, product_price, product_total, product_category]


# 获取折线图数据
def get_line_char(file):
    sales = []

    # 初始化
    len_c = len(cities)
    len_s = len(stay_in_current_city_years)

    # 初始化
    for i in range(len_s*len_c):
        sales.append(0)

    for row in file:
        if row[1] == "Product_ID":
            continue
        sales[cities.index(row[5])+stay_in_current_city_years.index(row[6])*len_c] += int(row[11])

    return sales


if __name__ == "__main__":
    # print(file_filter(read_file(), "1", "All", "All"))
    # print(file_filter_by_category(read_file(), "All", "All"))
    # print(get_line_char(file_filter(read_file(), "1", "All", "All")))
    print(cities * len(stay_in_current_city_years))
