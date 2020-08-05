import pandas as pd
import numpy as np


df = pd.read_csv('./CSV/t_asv.csv')
df_perBook = df.groupby(['b'])['t'].apply('  '.join).reset_index()

# print(df_perBook)

# print()
import csv

path = "./TXT/"

with open('./CSV/t_asv.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    currentBook = 1
    for row in csv_reader:
        # print(row[1], row[4])
        # if currentBook == row[1]:
        fileName = path + str(row[1]) + "_book.txt"
        f = open(fileName, "a+")
        
        append = row[4] + " "
        f.write(append)
        f.close()
        # else: 
        #   currentBook += 1
        #   fileName = path + str(currentBook) + ".txt"
        #   f = open(fileName, "a+")
        #   f.write(row[4])
        #   f.close()   

# export_csv = df_perBook.to_csv (r'export_dataframe.csv', index = None, header=True)






