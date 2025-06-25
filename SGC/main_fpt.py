import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import xml.etree.ElementTree as ET

def doc_file_excel(file_path):
    try:
        df = pd.read_excel(file_path, dtype={'Mã số thuế': str, 'Mã tra cứu': str, 'URL': str})
        
        # Tạo DataFrame với đầy đủ các cột cần thiết
        columns = {
            'Mã số thuế': 'mst',
            'Mã tra cứu': 'ma_tra_cuu',
            'URL': 'url',
            'Mã hóa đơn': 'ma_hoa_don',
            'Tên đơn vị bán hàng': 'ten_don_vi_ban',
            'Mã số thuế (bên bán)': 'mst_ban',
            'Địa chỉ (bên bán)': 'dia_chi_ban',
            'Điện thoại (bên bán)': 'dien_thoai_ban',
            'Số tài khoản (bên bán)': 'so_tai_khoan_ban',
            'Họ tên người mua hàng': 'ho_ten_mua',
            'Địa chỉ (bên mua)': 'dia_chi_mua',
            'Số tài khoản (bên mua)': 'so_tai_khoan_mua'
        }
        
        # Tạo DataFrame với tất cả các cột cần thiết
        df_result = pd.DataFrame(columns=columns.keys())
        
        # Đổi tên cột nếu cần
        df = df.rename(columns={
            'Mã số thuế': 'mst',
            'Mã tra cứu': 'ma_tra_cuu',
            'URL': 'url'
        })
        
        # Thêm các cột mới nếu chưa có
        for col in ['mst', 'ma_tra_cuu', 'url']:
            if col not in df.columns:
                df[col] = ''
        
        # Làm sạch dữ liệu
        df['mst'] = df['mst'].astype(str).str.strip()
        df['ma_tra_cuu'] = df['ma_tra_cuu'].astype(str).str.strip()
        df['url'] = df['url'].astype(str).str.strip()
        
        print(" Đã đọc dữ liệu từ input.xlsx")
        return df, df_result
    except Exception as e:
        print(f"Lỗi đọc file Excel: {e}")
        return pd.DataFrame(), pd.DataFrame()

def parse_xml_file(file_path):
    """Phân tích file XML và trích xuất thông tin hóa đơn"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Tạo cây phân tích XML
        root = ET.fromstring(content)
        
        # Khởi tạo từ điển lưu thông tin
        invoice_info = {}
        
        # Lấy thông tin cơ bản
        invoice_info['Mã hóa đơn'] = root.find('.//{*}SoHoaDon').text if root.find('.//{*}SoHoaDon') is not None else ''
        invoice_info['Ngày hóa đơn'] = root.find('.//{*}NgayHoaDon').text if root.find('.//{*}NgayHoaDon') is not None else ''
        
        # Thông tin bên bán
        seller = root.find('.//{*}NguoiBan')
        if seller is not None:
            invoice_info['Tên đơn vị bán hàng'] = seller.find('.//{*}Ten').text if seller.find('.//{*}Ten') is not None else ''
            invoice_info['Mã số thuế (bên bán)'] = seller.find('.//{*}MaSoThue').text if seller.find('.//{*}MaSoThue') is not None else ''
            invoice_info['Địa chỉ (bên bán)'] = seller.find('.//{*}DiaChi').text if seller.find('.//{*}DiaChi') is not None else ''
            invoice_info['Điện thoại (bên bán)'] = seller.find('.//{*}DienThoai').text if seller.find('.//{*}DienThoai') is not None else ''
            invoice_info['Số tài khoản (bên bán)'] = seller.find('.//{*}STKNHang').text if seller.find('.//{*}STKNHang') is not None else ''
        
        # Thông tin bên mua
        buyer = root.find('.//{*}NguoiMua')
        if buyer is not None:
            invoice_info['Họ tên người mua hàng'] = buyer.find('.//{*}Ten').text if buyer.find('.//{*}Ten') is not None else ''
            invoice_info['Mã số thuế (bên mua)'] = buyer.find('.//{*}MaSoThue').text if buyer.find('.//{*}MaSoThue') is not None else ''
            invoice_info['Địa chỉ (bên mua)'] = buyer.find('.//{*}DiaChi').text if buyer.find('.//{*}DiaChi') is not None else ''
            invoice_info['Số tài khoản (bên mua)'] = buyer.find('.//{*}STKNHang').text if buyer.find('.//{*}STKNHang') is not None else ''
        
        # Tổng tiền thanh toán
        invoice_info['Tổng tiền thanh toán'] = root.find('.//{*}TongTienThanhToan').text if root.find('.//{*}TongTienThanhToan') is not None else ''
        
        return invoice_info
    except Exception as e:
        print(f"Lỗi khi phân tích file {file_path}: {str(e)}")
        return None

try:
    # Khởi tạo trình duyệt
    print(" Đang khởi tạo trình duyệt...")
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-notifications')
    
    # Thêm tùy chọn để tắt thông báo lỗi certificate
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)  # Thời gian chờ mặc định
    
    # Đọc dữ liệu từ file Excel
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "input.xlsx")
    output_file = os.path.join(script_dir, "output.xlsx")
    
    print(f" Đang đọc dữ liệu từ: {input_file}")
    df, df_result = doc_file_excel(input_file)
    
    if df.empty:
        print(" Không có dữ liệu để xử lý.")
        exit()
    
    total = len(df)
    print(f" Bắt đầu tra cứu {total} hóa đơn...")
    
    for index, row in df.iterrows():
        mst = row['mst']
        ma_tra_cuu = row['ma_tra_cuu']
        url = row['url']
        
        print(f" Đang xử lý {index + 1}/{total}:")
        print(f"   - MST: {mst}")
        print(f"   - Mã tra cứu: {ma_tra_cuu}")
        print(f"   - URL: {url}")
        
        try:
            # Mở URL
            driver.get(url)
            
            # Đợi và điền MST
            try:
                mst_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//input[@placeholder="MST bên bán"]'))
                )
                mst_input.clear()
                mst_input.send_keys(mst)
                print("    Đã nhập MST")
            except Exception as e:
                print(f"    Lỗi khi nhập MST: {str(e)}")
                continue
            
            # Điền mã tra cứu
            try:
                ma_tc_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Mã tra cứu hóa đơn"]'))
                )
                ma_tc_input.clear()
                ma_tc_input.send_keys(ma_tra_cuu)
                print("    Đã nhập mã tra cứu")
            except Exception as e:
                print(f"   Lỗi khi nhập mã tra cứu: {str(e)}")
                continue
            
            # Nhấn nút tra cứu
            try:
                search_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Tra cứu")]'))
                )
                search_btn.click()
                print("    Đã nhấn nút tra cứu")
            except Exception as e:
                print(f"    Lỗi khi nhấn nút tra cứu: {str(e)}")
                continue
            
            # Chờ kết quả tải xong
            time.sleep(5)
            
            # Tải file XML
            try:
                download_link = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "Tải file XML")]'))
                )
                download_link.click()
                print("    Đã tải file XML")
            except Exception as e:
                print(f"    Lỗi khi tải file XML: {str(e)}")
                continue
            
            # Đọc file XML và trích xuất thông tin
            download_dir = os.path.join(script_dir, "download")
            xml_files = [f for f in os.listdir(download_dir) if f.endswith('.xml')]
            if xml_files:
                xml_file = xml_files[0]
                file_path = os.path.join(download_dir, xml_file)
                invoice_info = parse_xml_file(file_path)
                
                if invoice_info:
                    # Thêm kết quả vào DataFrame
                    result = {
                        'Mã số thuế': mst,
                        'Mã tra cứu': ma_tra_cuu,
                        'URL': url,
                        'Mã hóa đơn': invoice_info.get('Mã hóa đơn', ''),
                        'Tên đơn vị bán hàng': invoice_info.get('Tên đơn vị bán hàng', ''),
                        'Mã số thuế (bên bán)': invoice_info.get('Mã số thuế (bên bán)', ''),
                        'Địa chỉ (bên bán)': invoice_info.get('Địa chỉ (bên bán)', ''),
                        'Điện thoại (bên bán)': invoice_info.get('Điện thoại (bên bán)', ''),
                        'Số tài khoản (bên bán)': invoice_info.get('Số tài khoản (bên bán)', ''),
                        'Họ tên người mua hàng': invoice_info.get('Họ tên người mua hàng', ''),
                        'Địa chỉ (bên mua)': invoice_info.get('Địa chỉ (bên mua)', ''),
                        'Số tài khoản (bên mua)': invoice_info.get('Số tài khoản (bên mua)', '')
                    }
                    
                    df_result = pd.concat([df_result, pd.DataFrame([result])], ignore_index=True)
                    
                    # Lưu tạm kết quả sau mỗi lần xử lý
                    df_result.to_excel(output_file, index=False)
                    print(f"    Đã lưu kết quả tạm thởi")
                    
                    # Nghỉ giữa các lần truy vấn
                    time.sleep(2)
                    
        except Exception as e:
            print(f"    Lỗi khi xử lý hóa đơn: {str(e)}")
    
    print(f" Đã hoàn thành. Kết quả đã được lưu vào: {output_file}")
    
except Exception as e:
    print(f" Có lỗi xảy ra: {str(e)}")
    
finally:
    # Đóng trình duyệt
    if 'driver' in locals():
        driver.quit()
        print(" Đã đóng trình duyệt")