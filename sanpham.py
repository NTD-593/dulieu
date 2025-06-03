import pandas as pd


# 1. Đọc file CSV
df = pd.read_csv('sanpham.csv')
print(df)

# 2. Ghi dữ liệu vào file CSV
df.to_csv('sanpham.csv', index = False)

# 3. Lọc sản phẩm có giá > 15000
df_loc = df[df['Giá'] > 15000]

print("\nSản phẩm có giá > 15,000:")
print(df_loc)

# 4. Sắp xếp dữ liệu
df_sort = df.sort_values(by='Giá', ascending=False)
print("\nDữ liệu sắp xếp theo giá giảm dần: ")
print(df_sort)

# 5. Ghi danh sách lọc ra file mới
df_sort.to_csv('sanpham_moi.csv', index=False)
print("\nĐã ghi file sanpham_moi.csv thành công.")
df_loc.to_csv('sanpham_loc.csv', index=False)
print("\nĐã ghi file sanpham_loc.csv thành công.")

# 6. Tính tổng giá trị của các sản phẩm
tong_gia = df['Giá'].sum()
print("\nTổng giá trị của các sản phẩm: ", tong_gia)

# 7. Tính giá trị trung bình của các sản phẩm
gia_tri_trung_binh = df['Giá'].mean()
print("\nGiá trị trung bình của các sản phẩm: ", gia_tri_trung_binh)

# 8. Tính giá trị lớn nhất và nhỏ nhất
gia_tri_lon_nhat = df['Giá'].max()
gia_tri_nho_nhat = df['Giá'].min()
print("\nGiá trị lớn nhất: ", gia_tri_lon_nhat)
print("Giá trị nhỏ nhất: ", gia_tri_nho_nhat)