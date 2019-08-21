from scripts.funcs import pipeline_to_get_urn, create_df_for_urn_data_and_save
from pathlib import Path

# obter todas as urns referentes ao tribunal de contas da união
folder_to_look = Path("C:/Users/josefn/Documents/opensource/lxml-acervo/data")
if not folder_to_look.is_dir():
    raise ValueError("O path indicado não existe.")
years = list(range(2010, 2020))
tcu_urns = pipeline_to_get_urn(
    path=folder_to_look,
    years=years,
    patterns=["tribunal.contas.uniao"],
)

# salva o resultado em arquivos .csv
for data, year in zip(tcu_urns, years):
    if data:
        create_df_for_urn_data_and_save(data, f"tcu_{year}")
