from scripts.funcs import initiate_webdriver
from scripts.crawler import AcordaosTCU

years = [2015]
for year in years:
    browser = initiate_webdriver()
    acordaos = AcordaosTCU(browser)
    acordaos.get_urls(year)
    acordaos.parse_urls()
    acordaos.to_csv(f"./data/acordaos_{year}")