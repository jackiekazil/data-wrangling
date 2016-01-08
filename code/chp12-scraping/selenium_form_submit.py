from selenium import webdriver
from time import sleep


browser = webdriver.Firefox()
browser.get('http://google.com')

inputs = browser.find_elements_by_css_selector('form input')
for i in inputs:
    if i.is_displayed():
        search_bar = i
        break

search_bar.send_keys('web scraping with python')

search_button = browser.find_element_by_css_selector('form button')
search_button.click()

browser.implicitly_wait(10)
results = browser.find_elements_by_css_selector('div h3 a')

for r in results:
    action = webdriver.ActionChains(browser)
    action.move_to_element(r)
    action.perform()
    sleep(2)

browser.quit()
