from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

try:
    print("Đang truy cập trang web...")
    driver.get("https://thuvienphapluat.vn/ma-so-thue/tra-cuu-ma-so-thue-doanh-nghiep")
    
    print("Đang thu thập dữ liệu...")
    time.sleep(3)  
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "table.table tbody tr"))
    )
    
    data = []
    rows = driver.find_elements(By.CSS_SELECTOR, "table.table tbody tr")
    
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) >= 4: 
            data.append({
                "Tên doanh nghiệp": cols[2].text.strip(),
                "Mã số thuế": cols[1].text.strip(),
                "Ngày cấp": cols[3].text.strip()
            })
    
    if data:
        df = pd.DataFrame(data)
        df.to_csv("ma_so_thue.csv", encoding='utf-8-sig', index=False)
        print(f" Đã lưu {len(data)} bản ghi vào file ma_so_thue.csv")
    else:
        print("Không tìm thấy dữ liệu")

except Exception as e:
    print(f"Có lỗi xảy ra: {e}")

driver.quit()