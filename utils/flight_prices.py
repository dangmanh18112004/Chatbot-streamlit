# utils/flight_prices.py
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import streamlit as st
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager



def get_flight_prices(departure, destination, date):
    #url = f"https://www.skyscanner.com/transport/flights/{departure}/{destination}/{date}/?"
    # response = requests.get(url)
	
	# print(response)
	# if response.status_code != 200:
	# 	print("Không thể lấy dữ liệu, mã lỗi: ", response.status_code)
	# 	return None
	
	# soup = BeautifulSoup(response.text, 'html.parser')
	# try:
	# 	# Giả sử giá vé nằm trong thẻ HTML với class 'price'
	# 	price_tags = soup.find_all('span', class_='price').get_text()
		
	# 	return price_tags
	# 	# return float(price.replace('$', '').replace(',', ''))S
	# except AttributeError:
	# 	return None
    # return response
	driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
	
	# Mở trang Traveloka
	driver.get('https://www.traveloka.com/')
	st.write("DONE")
	input("Giải CAPTCHA rồi nhấn Enter để tiếp tục...")
	st.write("DONE")
	time.sleep(5)  # Đợi trang load xong
	

	# Tìm và nhập điểm đi
	departure_input = driver.find_element(By.ID, 'departure-input')
	departure_input.send_keys('Hà Nội')

	# Tìm và nhập điểm đến
	destination_input = driver.find_element(By.ID, 'destination-input')
	destination_input.send_keys('Hồ Chí Minh')

	# Chọn ngày bay (ví dụ chọn ngày 01/11/2024)
	date_input = driver.find_element(By.ID, 'departure-date-input')
	date_input.send_keys('2024-11-01')

	# Click vào nút tìm kiếm chuyến bay
	search_button = driver.find_element(By.CSS_SELECTOR, '.search-flight-button')
	search_button.click()

	# Chờ kết quả tìm kiếm được tải về
	time.sleep(10)  # Có thể cần điều chỉnh thời gian chờ
	
	# Tìm và nhập điểm đi
	departure_input = driver.find_element(By.ID, 'departure-input')
	departure_input.send_keys('Hà Nội')

	# Tìm và nhập điểm đến
	destination_input = driver.find_element(By.ID, 'destination-input')
	destination_input.send_keys('Hồ Chí Minh')

	# Chọn ngày bay (ví dụ chọn ngày 01/11/2024)
	date_input = driver.find_element(By.ID, 'departure-date-input')
	date_input.send_keys('2024-11-01')

	# Click vào nút tìm kiếm chuyến bay
	search_button = driver.find_element(By.CSS_SELECTOR, '.search-flight-button')
	search_button.click()

	# Chờ kết quả tìm kiếm được tải về
	time.sleep(10)  # Có thể cần điều chỉnh thời gian chờ

	prices = driver.find_elements(By.CSS_SELECTOR, "css-4rbku5 css-901oao r-a5wbuh r-b88u0q r-rjixqe r-fdjqy7")  # Điều chỉnh class phù hợp

	# In giá vé
	# for price in prices:
	# 	print(price.text)

	# Đóng trình duyệt
	driver.quit()
	return prices