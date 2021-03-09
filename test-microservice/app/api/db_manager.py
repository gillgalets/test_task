from app.api.db import database, metadata, engine
import sqlalchemy
import pandas as pd
import numpy as np
import shutil
import os
import openpyxl
from datetime import datetime
from fastapi import HTTPException

async def new_file(file, names = None, index_col = None, header = None):    #обрабатывает новый csv или xlsx файл
    '''

    :param file: input file
    :param names: list of names to use instead of default
    :param index_col: columns_names to create indexes
    :param header: row to get column names and start processing data
    :return: name of used table (new table if it was created and existing table if data was added)
    '''

    table_name, file_type = file.filename.split('.')
    if index_col[0] == '':
        index_col = None
    else:
        index_col = index_col[0].split(',')
    if names[0] == '':
        names = None
    else:
        names = names[0].split(',')
    if (file_type == 'xlsx'):
        with open("buffer.xlsx", "wb") as buffer:           #создает буфферный csv файл для удобства дальнейшей обработки
            shutil.copyfileobj(file.file, buffer)
        xlsx = openpyxl.load_workbook('buffer.xlsx')
        sheet = xlsx.active
        data = sheet.rows
        csv = open("buffer.csv", "w+")
        for row in data:                    #если файл в формате xlsx преобразовываем в csv
            l = list(row)
            for i in range(len(l)):
                if i == len(l) - 1:
                    csv.write(str(l[i].value))
                else:
                    csv.write(str(l[i].value) + ',')
            csv.write('\n')
        csv.close()
        os.remove('buffer.xlsx')
    if (file_type == 'csv'):
        with open("buffer.csv", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    try:
        with open('buffer.csv', 'r') as file:           #получаем пандас-датафрейм с указанием необходимых параметров
            data = pd.read_csv(file, names=names, header = header, index_col = index_col)
        os.remove('buffer.csv')
    except:
        os.remove('buffer.csv')
        raise HTTPException(status_code=412, detail="Wrong columns or indexes.")
    if (not index_col):
        index_col = ["id"]
    check = engine.has_table(table_name)   #проверка на существование таблицы с таким названием
    if check == True:                       #проверка, что в таблице с таким же названием такие же столбцы
        prev = pd.read_sql(table_name, con=engine)
        prev_columns = prev.columns.tolist()
        curr_columns = []
        curr_columns.extend(index_col)
        curr_columns.extend([x for x in data.columns.to_list() if x not in index_col])
        if (prev_columns != curr_columns):  #если таблица не соответствует существующей, добавляем таблицу с таким же названием + дата и время создания
            table_name = table_name+datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    data.to_sql(table_name, con=engine, index=True, index_label=index_col, if_exists='append')
    return table_name

async def get_table_names():            #возвращает список имен существующих таблиц
    metadata.reflect(engine)
    result = list(metadata.tables.keys())
    return result