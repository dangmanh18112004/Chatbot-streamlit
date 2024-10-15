# utils/flight_prices.py
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

def get_flight_prices(departure, destination, date):
    # url = "https://api.flightprices.com/v1/get-prices"  # Thay bằng URL của API thật sự
    # params = {
    #     "departure": departure,
    #     "destination": destination,
    #     "date": flight_date.strftime("%Y-%m-%d"),
    # }
    # headers = {
    #     "Authorization": "Bearer YOUR_API_KEY",  # Thay bằng API key nếu cần
    # }
    
    # try:
    #     response = requests.get(url, params=params, headers=headers)
    #     response.raise_for_status()  # Kiểm tra lỗi HTTP
    #     return response.json().get("prices")  # Giả định API trả về JSON với thông tin giá vé
    # except requests.exceptions.RequestException as e:
    #     return f"Lỗi khi gọi API: {e}"
	
	# url = f"https://www.skyscanner.com/transport/flights/{departure}/{destination}/{date}"
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
	
	driver = webdriver.Chrome()
	url = f"https://www.skyscanner.com/transport/flights/{departure}/{destination}/{date}"
	driver.get(url)
	
	time.sleep(10)
	html = driver.page_source
	driver.quit()
	soup = BeautifulSoup(html, 'html.parser')
	try:
		# Giả sử giá vé nằm trong thẻ HTML với class 'price'
		price_tags = soup.find_all('span', class_='price').get_text()
		
		return price_tags.text.strip()
		# return float(price.replace('$', '').replace(',', ''))S
	except AttributeError:
		return None