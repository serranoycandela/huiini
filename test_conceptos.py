import csv
import json
from os.path import join
path = "C:\\Users\\Jorge Cano\\Documents\\GitHub\\huiini"
with open(join(path,'formato_facturacion_3.3.csv'), encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    line_count_mal = 0
    cat_conceptos = {}
    for row in csv_reader:
        cat_conceptos[row[0]] = row[1]
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            try:
                print(row[1])
                line_count += 1
            except:
                print("no pude -------------------------------------------------------------")
                line_count_mal += 1
    print(f'Processed {line_count} lines. Con  {line_count_mal} malas')

    print(cat_conceptos["10151523"])


    with open (join(path,"conceptos.json"), "w") as outfile:
        json.dump (cat_conceptos,outfile)

#======================================================================================


with open(join(path,'catUsoCfdi.csv'), encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    line_count_mal = 0
    cat_usos = {}
    for row in csv_reader:
        cat_usos[row[1]] = row[2]

    print(cat_usos["D03"])


    with open (join(path,"catUsoCfdi.json"), "w") as outfile:
        json.dump (cat_usos,outfile)


#======================================================================================


with open(join(path,'catClavUnidad.csv'), encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    line_count_mal = 0
    cat_unida = {}
    for row in csv_reader:
        cat_unida[row[0]] = row[1]

    print(cat_unida["A41"])


    with open (join(path,"catClavUnidad.json"), "w") as outfile:
        json.dump (cat_unida,outfile)
