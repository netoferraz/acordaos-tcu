from configparser import ConfigParser
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException, InvalidArgumentException
from selenium.webdriver.support.ui import Select
from selenium.webdriver import Firefox, Chrome
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options as chromeOptions
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import selenium.webdriver.support.expected_conditions as EC
import selenium
from pathlib import Path
import re
from typing import List, Union, Text
import pandas as pd
from scripts.funcs import filter_elements_of_interest, coleta_dados_pagina_acordao
#configurations
config = ConfigParser()
config.read("config.ini")
driver = config['environment']['driver']
path_to_save_logs = Path("./logs/")
urls = pd.read_csv("./data/tcu_2017.csv")
urls = urls['url'].unique().tolist()
url = urls[0]
if not path_to_save_logs.is_dir():
    path_to_save_logs.mkdir(parents=True, exist_ok=True)
firefox_webelements = selenium.webdriver.firefox.webelement.FirefoxWebElement
browser = Firefox(executable_path=driver, service_log_path='./logs/geckodriver.log')
browser.get(url)
#localiza no dom os metadados
metadados_csssel = 'div.panel-body:nth-child(1)'
try:
    WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, metadados_csssel))
        )
except (NoSuchElementException, TimeoutException) as error:
    raise error("Não foi possível localizar os metadados")
else:
    metadados = browser.find_element_by_css_selector(metadados_csssel)

#armazena os metadados a exceção da urn (nome uniforme)
features = [elem.text for elem in metadados.find_elements_by_class_name("text-right")]
values = [elem.text for elem in metadados.find_elements_by_class_name("text-left")]
urn_object = {feature: value for feature, value in zip(features,values)}
urn_object['url_original'] = []
#localiza no dom o container de "Outras Publicações"
target_class = 'panel-body'
try:
    WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, target_class))
        )
except (NoSuchElementException, TimeoutException) as error:
    raise error("Não foi possível localizar os metadados")
else:
    target_container = browser.find_elements_by_class_name(target_class)

#coleta os links originais do normativo
filter_elems = filter_elements_of_interest(target_container, 'Tribunal de Contas da União (text/html)')
if filter_elems:
    if len(filter_elems) > 1:
        print("Há mais de dois elementos no filtro.")
    for elem in filter_elems:
        get_href = elem.find_elements_by_class_name("noprint")[0].get_attribute("href")
        urn_object['url_original'].append(get_href)

for href in urn_object['url_original']:
    browser.get(href)

#identificar se o elemento de ajuda está presente na página
pop_up_classname = 'body > app-root:nth-child(1) > ajuda:nth-child(3)'
try:
    WebDriverWait(browser, 10).until(
            EC.visibility_of(browser.find_element_by_css_selector(pop_up_classname))
        )
except (NoSuchElementException, TimeoutException) as error:
    #raise error("Não foi possível o popup de ajuda")
    print("Não há elemento de ajuda aberto na página")
else:
    elemento_ajuda = browser.find_element_by_css_selector(pop_up_classname)
    #fecha o elemento de ajuda
    elemento_ajuda.find_element_by_class_name("modal-close").click()

dados_acordao = coleta_dados_pagina_acordao(browser)
