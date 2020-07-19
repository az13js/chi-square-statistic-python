# -*- coding: UTF-8 -*-

import csv

file_name = 'data_stocks.csv'

def col_num(file_name):
    with open(file_name, newline='') as csv_file:
        for row in csv.reader(csv_file):
            return len(row)

def believe(chi_square):
    p = [0.5, 0.4, 0.25, 0.15, 0.1, 0.05, 0.025, 0.01, 0.005, 0.001]
    x = [0.455, 0.708, 1.323, 2.072, 2.706, 3.841, 5.024, 6.635, 7.879, 10.828]
    if chi_square < x[0]:
        return 0
    for i in range(len(p) - 1):
        if chi_square >= x[i] and chi_square < x[i + 1]:
            return 1 - p[i]
    return 0.999;

def analysis(file_name, k, no_eq=False):
    # 卡方统计表和变量对应关系
    # A B C
    # D E F
    # G H I
    A = B = C = D = E = F = G = H = I = 0
    # data_rows 列表保存一列的全部数据
    data_rows = []
    with open(file_name, newline='') as csv_file:
        for row in csv.reader(csv_file):
            data_rows.append(row[k - 1])
    row_total = len(data_rows)
    # 按照三个三个进行拆分
    sample_total = int((row_total - 1) / 3)
    # 每次取三行总数需要减去两行
    for j in range(sample_total):
        # 第一行表头不用处理
        i = j * 3 + 1
        event_A = float(data_rows[i + 1]) > float(data_rows[i])
        event_B = float(data_rows[i + 2]) > float(data_rows[i + 1])
        event_C = float(data_rows[i + 1]) < float(data_rows[i])
        event_D = float(data_rows[i + 2]) < float(data_rows[i + 1])
        if (no_eq and (not event_A) and (not event_C)) or ((not event_B) and (not event_D)):
            continue
        if event_A and event_B:
            A = A + 1
        if (not event_A) and event_B:
            B = B + 1
        if event_A and (not event_B):
            D = D + 1
        if (not event_A) and (not event_B):
            E = E + 1
    I = A + B + D + E
    C = A + B
    F = D + E
    G = A + D
    H = B + E
    print("卡方检验的表格：")
    print(A, B, C)
    print(D, E, F)
    print(G, H, I)
    squre = A * E - B * D
    chi_square = squre / C / F * squre / G / H * I
    believe_value = believe(chi_square) * 100
    print("卡方统计量是：" + str(chi_square))
    print("有百分之 %.3f 的把握认为第 %d 列的数据前后变化存在关联关系" %(believe_value, k))

K = col_num(file_name)
print("文件 \"%s\" 一共有 %d 列。" %(file_name, K))

for k in range(1, K + 1):
    # k=1时第1列不分析
    if k > 1:
        print("分析第 %d 列的数据" %(k))
        analysis(file_name, k)
        print("--------------------完成--------------------");
