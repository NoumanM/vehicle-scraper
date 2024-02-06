from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests
import os
import time
import datetime

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
date_today = datetime.datetime.now().strftime("%d-%m-%Y")
print("Today Date: ", date_today)
def get_driver():
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    chrome_options = Options()
    chrome_options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(service=Service(executable_path=ChromeDriverManager().install()), options=chrome_options)
    driver.maximize_window()
    return driver


def download_images(image_urls, folder_name, save_path):
    folder_path = os.path.join(save_path, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    for idx, url in enumerate(image_urls, start=1):
        file_name = f'image{idx}.jpg'
        file_path = os.path.join(folder_path, file_name)
        for j in range(0, 2):
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    with open(file_path, 'wb') as file:
                        file.write(response.content)
                        break
                else:
                    print(f'Failed to download {file_name}')
            except:
                print(f'Failed to download {file_path}')


all_data = []
urls = []
driver = get_driver()
for pg in range(1, 3):
    driver.get(f"https://tampaautosource.com/inventory/{pg}")
    driver.implicitly_wait(10)
    urls = urls + [l.get_attribute("href") for l in driver.find_elements(By.XPATH,
                                                                         ".//div[@class='inv-box-hovers  pure-u-lg-1-4 pure-u-md-1-3 pure-u-sm-1-2 pure-u-1']/div/a")]
    time.sleep(1)

for url in urls:
    data = {}
    driver.get(url)
    driver.implicitly_wait(10)
    time.sleep(1)
    try:
        data['Name'] = driver.find_element(By.XPATH, ".//h1").text.strip()
    except:
        data['Name'] = ''
    try:
        data['Year'] = driver.find_element(By.XPATH, "//span[contains(text(), 'Year')]/..").text.replace('Year: ', '')
    except:
        data['Year'] = ''
    try:
        data['Make'] = driver.find_element(By.XPATH, "//span[contains(text(), 'Make')]/..").text.replace("Make: ", '')
    except:
        data['Make'] = ''
    try:
        data['Model'] = driver.find_element(By.XPATH, "//span[contains(text(), 'Model')]/..").text.replace("Model: ",
                                                                                                           '')
    except:
        data['Model'] = ''
    try:
        data['Description'] = driver.find_element(By.XPATH, "//div[@class='tab-content description']").text.strip()
    except:
        data['Description'] = ''
    try:
        data['Price'] = driver.find_element(By.XPATH, ".//div[@class='price-tag']/span").text.strip()
    except:
        data['Price'] = ''
    try:
        data['Mileage'] = driver.find_element(By.XPATH, "//span[contains(text(), 'Mileage:')]/..").text.replace(
            "Mileage: ", '')
    except:
        data['Mileage'] = ''
    try:
        data['Body Style'] = driver.find_element(By.XPATH, "//span[contains(text(), 'Body Style:')]/..").text.replace(
            "Body Style: ", '')
    except:
        data['Body Style'] = ''
    try:
        data['Fuel'] = driver.find_element(By.XPATH, "//span[contains(text(), 'Fuel')]/..").text.replace("Fuel: ", '')
    except:
        data['Fuel'] = ''
    try:
        data['sales-price'] = driver.find_element(By.XPATH, ".//div[@class='sales-price']/s").text.strip()
    except:
        data['sales-price'] = ''
    try:
        data['VIN'] = driver.find_element(By.XPATH, ".//span[contains(text(), 'VIN:')]/..").text.replace("VIN: ", '')
    except:
        data['VIN'] = ''
    try:
        data['Trim'] = driver.find_element(By.XPATH, "//span[contains(text(), 'Trim')]/..").text.replace("Trim: ", '')
    except:
        data['Trim'] = ''
    try:
        data['Trans'] = driver.find_element(By.XPATH, "//span[contains(text(), 'Trans')]/..").text.replace("Trans: ",
                                                                                                           '')
    except:
        data['Trans'] = ''
    try:
        data['Ext. Color'] = driver.find_element(By.XPATH, "//span[contains(text(), 'Ext. Color:')]/..").text.replace(
            "Ext. Color: ", '')
    except:
        data['Ext. Color'] = ''
    try:
        data['Int. Color'] = driver.find_element(By.XPATH, "//span[contains(text(), 'Int. Color:')]/..").text.replace(
            "Int. Color: ", '')
    except:
        data['Int. Color'] = ''
    try:
        data['Engine'] = driver.find_element(By.XPATH, "//span[contains(text(), 'Engine:')]/..").text.replace(
            "Engine: ", '')
    except:
        data['Engine'] = ''
    try:
        data['MPG'] = driver.find_element(By.XPATH, "//span[contains(text(), 'MPG:')]/..").text.replace("MPG: ", '')
    except:
        data['MPG'] = ''
    try:
        data['New / Used'] = driver.find_element(By.XPATH, "//span[contains(text(), 'New / Used:')]/..").text.replace(
            "New / Used: ", '')
    except:
        data['New / Used'] = ''
    try:
        data['address'] = driver.find_elements(By.XPATH, "//div[@class='address']")[2].text.strip().replace('\n', ' ')
    except:
        data['address'] = ''
    try:
        data['Url'] = url
    except:
        data['Url'] = ''
    try:
        data['Images'] = [li.get_attribute("style").split("url(\"")[1].split("?")[0].replace("\")", "") for li in
                          driver.find_elements(By.XPATH, "//div[@class='img-wrapper pure-g']/div/div")]
    except:
        data['Images'] = []

    # Append the data to the list
    print('Data appended for ', data['Name'])
    all_data.append(data)
df = pd.DataFrame(all_data)


def clean_price(price):
    price = price.replace('$', '').replace(',', '')
    return int(float(price))


df['Price'] = df['Price'].apply(clean_price)

def fix_colour(color):
    if 'Sil' == color:
        return 'Silver'
    elif 'Blk' == color:
        return 'Black'
    elif 'Brownn' == color:
        return 'Brown'
    elif color == 'Tann':
        return 'Tan'
    else:
        return color

def clean_body_style(style):
    if 'SUV' in style:
        return 'SUV'
    elif 'Sedan' in style:
        return 'Sedan'
    else:
        return 'SUV'


df['Body Style'] = df['Body Style'].apply(clean_body_style)
df['Int. Color'] = df['Int. Color'].apply(fix_colour)
df['Trans'] = df['Trans'].str.replace('Auto', 'Automatic transmission', case=False)
df['Trans'] = df['Trans'].str.replace('Manual', 'Manual transmission', case=False)
df['Fuel'] = df['Fuel'].str.replace('Gas', 'Gasoline', case=False)
df['Ext. Color'] = df['Ext. Color'].apply(fix_colour)


desired_path = rf'{BASE_DIR}/Inventory-{date_today}'
if not os.path.exists(desired_path):
    os.mkdir(desired_path)
file_path = os.path.join(BASE_DIR, rf"Scrapped-data-tampa-{date_today}.csv")
# Save the DataFrame as a CSV file
df.to_csv(file_path, index=False)

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    folder_name = f'{row["Name"]} {row["Ext. Color"]}'
    print('Downloading Images for ', folder_name)
    download_images(row["Images"], folder_name, desired_path)
driver.quit()
print("Scrapped Succesfully")
