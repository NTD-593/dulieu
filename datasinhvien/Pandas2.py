import pandas as pd
import numpy as np

data = {
    'ID': [101, 102, 103, 104, 105, 106],
    'Name': ['An', 'Bình', 'Cường', 'Dương', np.nan, 'Hạnh'],
    'Age': [25, np.nan, 30, 22, 28, 35],
    'Department': ['HR', 'IT', 'IT', 'Finance', 'HR', np.nan],
    'Salary': [700, 800, 750, np.nan, 710, 770]
}
df_nv = pd.DataFrame(data)

data_pb = {
    'Department': ['HR', 'IT', 'Finance', 'Marketing'],
    'Manager': ['Trang', 'Khoa', 'Minh', 'Lan']
}
df_pb = pd.DataFrame(data_pb)

print("Số giá trị thiếu trong mỗi cột:")
print(df_nv.isnull().sum())

df_nv = df_nv[df_nv.isnull().sum(axis=1) <= 2]

df_nv['Name'].fillna('Chưa rõ', inplace=True)
df_nv['Age'].fillna(df_nv['Age'].mean(), inplace=True)
df_nv['Salary'].fillna(method='ffill', inplace=True)  
df_nv['Department'].fillna('Unknown', inplace=True)

df_nv['Age'] = df_nv['Age'].astype(int)
df_nv['Salary'] = df_nv['Salary'].astype(int)

df_nv['Salary_after_tax'] = df_nv['Salary'] * 0.9

it_employees = df_nv[(df_nv['Department'] == 'IT') & (df_nv['Age'] > 25)]
print("\n Nhân viên IT trên 25 tuổi:")
print(it_employees)

df_nv_sorted = df_nv.sort_values('Salary_after_tax', ascending=False)
print("\nBảng nhân viên sau khi sắp xếp:")
print(df_nv_sorted)

avg_salary = df_nv.groupby('Department')['Salary'].mean()
print("\n Lương trung bình theo phòng ban:")
print(avg_salary)

df_merged = pd.merge(df_nv, df_pb, on='Department', how='left')
print("\n Bảng sau khi nối với thông tin quản lý:")
print(df_merged)

new_NV = pd.DataFrame({
    'ID': [107, 108],
    'Name': ['Giang', 'Hùng'],
    'Age': [27, 31],
    'Department': ['IT', 'Marketing'],
    'Salary': [780, 820]
})
df_nv = pd.concat([df_nv, new_NV], ignore_index=True)
print("\n Bảng sau khi thêm nhân viên mới:")
print(df_nv)
