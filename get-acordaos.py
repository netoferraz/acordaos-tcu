from scripts.funcs import initiate_webdriver
from scripts.crawler import AcordaosTCU

browser = initiate_webdriver()
acordaos = AcordaosTCU(browser)
acordaos.get_urls()
acordaos.parse_urls()
