from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import pandas as pd
import os
import time

EXCEL_FILE = "AHoaDon/dataFull/data.xlsx"  
WAIT_TIME = 10  
DOWNLOAD_DIR = os.path.abspath("AHoaDon")  

def setup_driver():
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    
    chrome_options = Options()
    prefs = {
        "download.default_directory": DOWNLOAD_DIR,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def xu_ly_hoa_don(driver, ma_hoa_don, link_tra_cuu):
    try:
        driver.get(link_tra_cuu)
        
        wait(driver, WAIT_TIME).until(EC.presence_of_element_located((By.ID, "txtCode"))).clear()
        wait(driver, WAIT_TIME).until(EC.presence_of_element_located((By.ID, "txtCode"))).send_keys(ma_hoa_don)
        wait(driver, WAIT_TIME).until(EC.element_to_be_clickable((By.ID, "btnSearchInvoice"))).click()
        
        download_btn = wait(driver, WAIT_TIME).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.res-btn.download")))
        driver.execute_script("arguments[0].click();", download_btn)
        
        pdf_button = wait(driver, WAIT_TIME).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.dm-item.pdf.txt-download-pdf")))
        driver.execute_script("arguments[0].click();", pdf_button)
        
        print(f"Đã gửi yêu cầu tải hóa đơn {ma_hoa_don}")
        time.sleep(5)       
        return True
        
    except Exception as e:
        print(f"Lỗi: {str(e)}")
        return False

if __name__ == "__main__":
    try:
        df = pd.read_excel(EXCEL_FILE)
        thanh_cong = 0
        driver = setup_driver()
        
        try:
            for index, row in df.iterrows():
                ma = str(row["Ma_Hoa_Don"]).strip()
                link = str(row["Trang_Tra_Cuu"]).strip()
                
                if xu_ly_hoa_don(driver, ma, link):
                    thanh_cong += 1
                else:
                    print(f"Không thể tải hóa đơn: {ma}")
                
                time.sleep(5)  
            
            print(f"\nĐã xử lý xong: {thanh_cong}/{len(df)} hóa đơn")
            print(f"File đã được lưu vào thư mục: {os.path.abspath(DOWNLOAD_DIR)}")
            
        finally:
            driver.quit()
            
    except Exception as e:
        print(f"Có lỗi xảy ra: {str(e)}")