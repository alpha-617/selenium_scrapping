from seleniumwire import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
from selenium.webdriver.common.by import By
import json
 
 
desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

options = webdriver.ChromeOptions()
 
options.add_argument("--no-sandbox")
options.add_argument("--headless")
options.add_argument('--disable-dev-shm-usage')
options.add_argument("start-maximized")
options.add_argument("--autoplay-policy=no-user-gesture-required")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--mute-audio")
options.add_argument("--disable-notifications")
options.add_argument("--disable-popup-blocking")
options.add_argument(f'user-agent={desired_capabilities}')

 
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                           options=options)
 
 # Create a request interceptor
def interceptor(request):
    del request.headers['Referer']  # Delete the header first
    request.headers['Referer'] = 'my_referer'
# Set the interceptor on the driver
driver.request_interceptor = interceptor

url = "http://127.0.0.1/my_url/"
driver.get(url)
wait = WebDriverWait(driver, 20*60)
# element = wait.until(EC.element_to_be_clickable((By.XPATH,'//button[contains(@onclick,"skipAd()")]')))  //optional
# element.click()

def get_m3u8_urls(url): 
   # driver.get(url)
   # driver.find_element(By.XPATH,'//button[contains(@onclick,"skipAd()")]').click()
   driver.execute_script("window.scrollTo(0, 10000)")
   time.sleep(10)
   logs = driver.get_log("performance")
   url_list = []
  
   for log in logs:
       network_log = json.loads(log["message"])["message"]
       if ("Network.response" in network_log["method"]
           or "Network.request" in network_log["method"]
           or "Network.webSocket" in network_log["method"]):
           if 'request' in network_log["params"]:
               if 'url' in network_log["params"]["request"]:
                   if 'm3u8' in network_log["params"]["request"]["url"] or '.mp4'  in network_log["params"]["request"]["url"]:
                       if "blob" not in network_log["params"]["request"]["url"]:
                           if '.m3u8' in network_log["params"]["request"]["url"]:
                               url_list.append( network_log["params"]["request"]["url"] )


   data = '[{}]'.format('\n'.join(url_list))
   text_file = open("output.txt", "w")
   text_file.write(data)
     
   driver.close()
   return url_list
 
 
if __name__ == "__main__":

   url_list = get_m3u8_urls(url)
   # with open("output.txt", "w") as outfile:
   #      json.dump(url_list, outfile)
   print(url_list)
