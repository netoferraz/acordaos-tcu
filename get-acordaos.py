from scripts.crawler import AcordaosTCU
from configparser import ConfigParser
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox
from pathlib import Path

#configuracoes
config = ConfigParser()
config.read("config.ini")
driver = config["driver"]["driver"]
options = Options()
options.headless = True
path_to_save_logs = Path(config["driver"]["driver_logs"])
if not path_to_save_logs.parent.is_dir():
    path_to_save_logs.mkdir(parents=True, exist_ok=True)
#inicializa uma instância do driver
browser = Firefox(
    executable_path=driver, service_log_path=path_to_save_logs, options=options
)

acordaos = AcordaosTCU(browser)
#years = list(range(2000, 2010))
years = [2008]
acordaos.get_urls(years)
acordaos.parse_urls()
if len(years) != 1:
    min_year, max_year = min(years), max(years)
    acordaos.to_csv(f"./data/acordaos_{min_year}_to_{max_year}")
acordaos.to_csv(f"./data/acordaos_{year}")
