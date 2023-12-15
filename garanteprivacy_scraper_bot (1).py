#!/usr/bin/env python
# coding: utf-8

# In[8]:


from time import sleep
from requests import options
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
from fake_useragent import UserAgent
import random
from random import randint
from selenium.webdriver.common.keys import Keys
import string
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC


# In[25]:


url = 'https://www.garanteprivacy.it/home/ricerca/-/search/key/d'


# In[10]:


from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome()
driver.get(url)


# In[32]:


title = []
link = []
file_link = []
date = []


# In[33]:


choice = int(input("Enter 1 to choose dates option else press 0 to skip it : "))
if choice == 1:
    def convert_date_format(input_date):
        # Convert date from yyyy-mm-dd to mm/dd/yyyy format
        parts = input_date.split("-")
        return f"{parts[1]}/{parts[2]}/{parts[0]}"
    # Find the date input field using its ID
    date_input = driver.find_element(By.ID, "_g_gpdp5_search_GGpdp5SearchPortlet_dataInizio")

    # Clear the existing value (optional)
    date_input.clear()

    # Enter the desired date
    desired_date = input("Enter starting date using format (yyyy-mm-dd) ")  # Replace this with the date you want to enter
    formatted_date = convert_date_format(desired_date)
    date_input.send_keys(formatted_date)

    # Trigger the 'onchange' event (optional, if the date input has any event tied to it)
    date_input.send_keys(Keys.TAB)

    # Wait for a short time (optional, you can adjust this based on the page's behavior)
    time.sleep(1)

    # Find the date input field using its ID
    date_input = driver.find_element(By.ID, "_g_gpdp5_search_GGpdp5SearchPortlet_dataFine")

    # Clear the existing value (optional)
    date_input.clear()

    # Enter the desired date
    desired_date = input("Enter ending date using format (yyyy-mm-dd) ")  # Replace this with the date you want to enter
    formatted_date = convert_date_format(desired_date)
    date_input.send_keys(formatted_date)

    # Trigger the 'onchange' event (optional, if the date input has any event tied to it)
    date_input.send_keys(Keys.TAB)

    # Wait for a short time (optional, you can adjust this based on the page's behavior)
    time.sleep(1)


# In[34]:


driver.find_element(By.ID, '_g_gpdp5_search_GGpdp5SearchPortlet_bottoneArgomento').click()
time.sleep(1.5)


# In[35]:


driver.find_element(By.ID, '8963834_anchor').click()
time.sleep(1.5)


# In[36]:


driver.find_element(By.CLASS_NAME, 'btn.w-100.btn-secondary.bg-grigio-filtro.submitRicerca.text-uppercase').click()


# In[37]:


time.sleep(5)


# In[38]:


query = driver.find_element(By.ID, '_g_gpdp5_search_GGpdp5SearchPortlet_text')
query.clear()
query.send_keys(input("Enter the query to search : "))


# In[ ]:


time.sleep(3)
driver.find_element(By.CLASS_NAME, 'btn.w-100.btn-secondary.bg-grigio-filtro.submitRicerca.text-uppercase').click()
time.sleep(2)


# In[ ]:


while True:
    time.sleep(4)
    for i in driver.find_elements(By.CLASS_NAME, 'titolo-risultato.text-justify'):
        title.append(i.get_attribute('title'))
        link.append(i.get_attribute('href'))
    try:
        driver.find_elements(By.CLASS_NAME, 'page-item')[len(driver.find_elements(By.CLASS_NAME, 'page-item')) -1].click()
    except:
        break


# In[ ]:


for i in link:
    driver.get(i)
    for j in driver.find_elements(By.CLASS_NAME, 'col'):
        if(j.text.find('Data') != -1):
            date.append(j.text.split()[1])
            break
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # Find all form elements
    form_elements = soup.find_all('form')

    # Define a pattern to match the PDF link in the form action
    pattern = r'https:\/\/www\.garanteprivacy\.it:443\/pdf\?p_p_id=PdfUtil.+_PdfUtil_articleId=\d+'
    
    for form_element in form_elements:
        form_action = form_element.get('action')
        match = re.search(pattern, form_action)
        if match:
            file_link.append(match.group(0))
            break


# In[ ]:


# Create a dictionary to store the data
data = {
    'Title': title,
    'Link': link,
    'File_Link': file_link,
    'Date': date
}

# Convert the dictionary to a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame as a CSV file
df.to_csv('data.csv', index=False)


# In[ ]:


df


# In[ ]:




