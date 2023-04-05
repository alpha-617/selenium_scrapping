from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import sys

options = FirefoxOptions()
options.add_argument("--headless")
 
browser = webdriver.Firefox()

opts = FirefoxOptions()
opts.add_argument("--headless")

browser = webdriver.Firefox(options=opts)

try:
# Online
 browser.get('http://your_url')
except:
    print("Referer Gagal")
    browser.quit()
    sys.exit(1)

try:
 browser.find_element(By.XPATH,'//a[contains(@href,"movie2/168/single-live?watch=1")]').click()
except:
    print("Nothing to click !")
    sys.exit(1)   

# wait(browser, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[style='width:100%; height:480px;']")))  Hasil Boolean

try:
 with open('out.txt', 'w') as f:    
  element=WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='uk-cover uk-margin-top']/iframe[@src]"))).get_attribute("src")
  print(element)
  f.write(element)
except:
    print("No src")
    sys.exit(1)

browser.quit()

