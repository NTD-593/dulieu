import pandas as pd

data = {
    'Name':['Dat','Huy','Nam','Hoa','Hien','Hanh','Hieu','Huong','Hai','Huyen'],
    'Age':[20,21,22,23,24,25,26,27,28,29],
    'Gender':['Nam','Nam','Nam','Nữ','Nam','Nữ','Nam','Nữ','Nam','Nữ'],
    'Score':[8.5,9.0,2.2,8.5,7.0,4.4,10.0,8.2,3.7,9.0]
}
df_sinhvien = pd.DataFrame(data)
df_sinhvien.index = range(1,len(df_sinhvien)+1)

print("In toàn bộ danh sách sinh viên")
print(df_sinhvien)

print("In 3 sinh viên đầu tiên")
print(df_sinhvien.head(3))

print("Index = 2, cột name ")
print(df_sinhvien.loc[2,'Name'])

print("Index = 10, cột Age")
print(df_sinhvien.loc[10,'Age'])

print("In Name và Score")
print(df_sinhvien[['Name','Score']])

df_sinhvien['Pass'] = df_sinhvien['Score'] >= 5
print("Thêm cột True/False vào danh sách")
print(df_sinhvien)

print("Sắp xếp theo Score giảm dần")
df_sinhvienSX = df_sinhvien.sort_values(by='Score', ascending=False)
print(df_sinhvienSX)