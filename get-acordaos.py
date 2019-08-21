from scripts.crawler import AcordaosTCU
from configparser import ConfigParser
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox
from pathlib import Path

config = ConfigParser()
config.read("config.ini")
driver = config["environment"]["driver"]
years = list(range(2015, 2018))

options = Options()
#options.headless = True
path_to_save_logs = Path("./logs/")
if not path_to_save_logs.is_dir():
    path_to_save_logs.mkdir(parents=True, exist_ok=True)

browser = Firefox(
    executable_path=driver, service_log_path="./logs/geckodriver.log", options=options
)

acordaos = AcordaosTCU(browser)
acordaos.get_urls(years)
acordaos.parse_urls()
min_year, max_year = min(years), max(years)
acordaos.to_csv(f"acordaos_{min_year}_to_{max_year}")
