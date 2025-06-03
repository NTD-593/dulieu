import pandas as pd

data = {
    'Tên':['Nguyễn Văn A','Nguyễn Văn B','Nguyễn Văn C'],
    'Tuổi':[20,21,22],
    'Giới tính':['Nam','Nữ','Nam']
}
df = pd.DataFrame(data)
print(df)
print(df['Tên'])
print(df['Tuổi'])
print(df['Giới tính'])


# Ghi dữ liệu ra file CSV mới
df.to_csv('test.csv', index=False)