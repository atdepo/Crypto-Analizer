from bs4 import BeautifulSoup
import time
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from valute import Valuta


def get_stacks():
    r = requests.get("https://www.gate.io/trade/stx_usdt")
    soup = BeautifulSoup(r.text, 'html.parser')
    elem = soup.find("i", attrs={"id": "currPrice"})
    to_return = "stacks : " + elem.text + " at [" + datetime.now().strftime("%H:%M:%S") + "]"
    print(to_return)
    return to_return


def get_valore(valuta):
    chrome = "C:\Program Files\Google\Chrome\chromedriver.exe"
    chrome_option = Options()
    chrome_option.add_argument("--headless")
    browser = webdriver.Chrome(chrome, options=chrome_option)
    browser.get("https://www.coinbase.com/it/price/" + valuta)
    delay = 15
    try:
        WebDriverWait(browser, delay).until(ec.presence_of_element_located((By.CLASS_NAME, 'fQDZTy')))
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        price = soup.find('span', attrs={"class": "fQDZTy"})
        to_return = (valuta + ": " + price.text[0:-1] + " at [" + datetime.now().strftime("%H:%M:%S") + "]", price.text)
        print(to_return[0])
        return to_return
    except TimeoutException:
        print("Loading took too much time!")


if __name__ == '__main__':

    while True:
        btc = get_valore(Valuta.bitcoin)[1]
        btc = btc[:btc.find('\'')]


        print(btc)
        data = {"btc": btc,
                "stl": get_valore(Valuta.stellar)[1],
                "bat": get_valore(Valuta.bat)[1],
                "etc": get_valore(Valuta.eth_classic)[1],
                "stx": get_stacks()}

        requests.post("http://localhost:8080/update", json=data)
        time.sleep(300)
