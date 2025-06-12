from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

driver = webdriver.Chrome()

users = [
    {"username": "standard_user", "password": "secret_sauce"},
    {"username": "locked_out_user", "password": "secret_sauce"},
    {"username": "problem_user", "password": "secret_sauce"},
    {"username": "performance_glitch_user", "password": "secret_sauce"},
    {"username": "error_user", "password": "secret_sauce"},
    {"username": "visual_user", "password": "secret_sauce"}
]

all_products = []

try:
    for user in users:
        print(f"Đang thử đăng nhập với: {user['username']}")
        
        driver.get("https://www.saucedemo.com")
        time.sleep(1)
        
        driver.find_element(By.ID, "user-name").send_keys(user["username"])
        driver.find_element(By.ID, "password").send_keys(user["password"])
        driver.find_element(By.ID, "login-button").click()
        time.sleep(1)
        
        if "inventory" in driver.current_url:
            print(f"Đăng nhập thành công: {user['username']}")
            
            products = driver.find_elements(By.CLASS_NAME, "inventory_item")
            print(f"Tìm thấy {len(products)} sản phẩm")
            
            for product in products:
                all_products.append({
                    "Tài khoản": user["username"],
                    "Sản phẩm": product.find_element(By.CLASS_NAME, "inventory_item_name").text,
                    "Giá": product.find_element(By.CLASS_NAME, "inventory_item_price").text
                })
            
            driver.find_element(By.ID, "react-burger-menu-btn").click()
            time.sleep(0.5)
            driver.find_element(By.ID, "logout_sidebar_link").click()
            time.sleep(0.5)
            
        else:
            try:
                error = driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']").text
                print(f"Đăng nhập thất bại: {error}")
            except:
                print(f"Đăng nhập thất bại: {user['username']}")

except Exception as e:
    print(f"Có lỗi xảy ra: {e}")

finally:
    if all_products:
        pd.DataFrame(all_products).to_csv("saucedemo_products.csv", index=False, encoding='utf-8-sig')
        print(f"Đã lưu {len(all_products)} sản phẩm vào file saucedemo_products.csv")
    
    driver.quit()