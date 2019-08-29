from scripts.funcs import pipeline_to_get_urn, create_df_for_urn_data_and_save
from pathlib import Path
from configparser import ConfigParser
config = ConfigParser()
config.read("config.ini")
urn_path = config["paths"]["urn_path"]
# obter todas as urns referentes ao tribunal de contas da união
folder_to_look = Path(urn_path)
if not folder_to_look.is_dir():
    raise ValueError("O path indicado não existe.")
years = list(range(1992, 2000))
tcu_urns, filtered_years = pipeline_to_get_urn(
    path=folder_to_look,
    years=years,
    patterns=["tribunal.contas.uniao"],
)

# salva o resultado em arquivos .csv
for data, year in zip(tcu_urns, filtered_years):
    if data:
        create_df_for_urn_data_and_save(data, f"tcu_{year}")
