import xlrd as excel
import numpy as np

path = "C:/Users/Pankaja Suganda/Documents/VS Code/Plant Growth Research/plant growth rate project_1.xlsx"
groups = np.array(['Group 01','Group 02','Group 03','Group 04','Group 05'])
workbook = excel.open_workbook(path)

data = []

for k in range(0,5):
    sheet = workbook.sheet_by_name(groups[k])
    for j in range(2,17,2):
        for i in range(4,sheet.nrows):
            data.append([k+1,i-3,sheet.cell_value(i,j),sheet.cell_value(i,j+1)]) # group, day, leafcount, height
np.savetxt("Plant Growth Research/Plant_Growth_Data.csv", data, delimiter=",",fmt='%d',header='Group,Day,Leaf_Count,Height',comments='')
print ('done')
