import os
import pandas as pd
import json
import re
import gc
from typing import List, Dict, Union
from numbers import Number
from pathlib import Path

def parse_json_year_date(year: Number, fullpath: Path) -> Union[Path, None]:
    """
    Filtra os arquivos json por ano.
    """
    if not isinstance(fullpath, Path):
        raise TypeError("O parâmetro path deve do tipo Path.")
    pattern_finder = re.search(f"_{year}\.json", fullpath.name)
    if pattern_finder:
        return fullpath
    else:
        return None


def load_into_dataframe(jsonFile: List[Dict]) -> pd.DataFrame:
    """
    Cria uma DataFrame a partir de uma lista de dicionários (JSON).
    """
    # container para armazenar arquivos json
    container_of_json = []
    for file in jsonFile:
        with open(file, "r", encoding='utf8') as f:
            d = json.load(f)
            container_of_json.append(d)
    # container of dataframes
    container_of_dataframes = []
    for data in container_of_json:
        df = pd.read_json(json.dumps(data), orient="records", encoding="utf8")
        container_of_dataframes.append(df)
    df = pd.concat(container_of_dataframes)
    return df


def get_urn(pattern: str, df: pd.DataFrame) -> Dict:
    """
    Recebe padrão de urn e coleta todos as ocorrências no dataframe.
    """
    urn_container = {}
    for index, row in df.iterrows():
        if type(row["urn"]) == list:
            for data in row["urn"]:
                if pattern in data:
                    if pattern in urn_container:
                        continue
                    else:
                        urn_container[row["urn"]] = row["url"]
        else:
            if pattern in row["urn"]:
                if pattern in urn_container:
                    continue
                else:
                    urn_container[row["urn"]] = row["url"]
    return urn_container


def select_files_based_on_year(path: Path, year: str) -> List[Path]:
    """
    Seleciona os arquivos baseado no ano indicado em seus respectivos nomes.
    """
    if not isinstance(path, Path):
        raise TypeError("O parâmetro path deve do tipo Path.")
    container_of_json_year = []
    for dirname, _, filenames in os.walk(path):
        for filename in filenames:
            path_filename = Path(os.path.join(dirname, filename))
            check_pattern = parse_json_year_date(year, path_filename)
            if check_pattern:
                container_of_json_year.append(path_filename)
    return container_of_json_year


def pipeline_to_get_urn(path: Path, years: List[str], patterns: List[str]) -> List[Dict]:
    """
    Pipeline para coletar as urns de um determinado padrão ao longo de vários arquivos.
    
    Atributos:
        path: diretório onde estão os arquivos json
        years: list de anos que se deseja coletar os dados
        pattern: a substring oriunda de uma URN que se deseja buscar
    """
    if not isinstance(path, Path):
        raise TypeError("O parâmetro path deve do tipo Path.")
    container = []
    if not isinstance(years, List):
        raise TypeError("O parâmetro years precisa ser uma lista.")
    if not isinstance(patterns, List):
        raise TypeError("O parâmetro patterns precisa ser uma lista.")
    for year in years:
        container_of_json_year = select_files_based_on_year(path, year)
        # sort by filename
        container_of_json_year = sorted(
            container_of_json_year, key=lambda x: int(x.name.split("_")[0])
        )
        # carrega os dados
        df = load_into_dataframe(container_of_json_year)
        for pattern in patterns:
            print(
                f"Iniciando a coleta das urn para o padrão {pattern} na base anual {year}."
            )
            urn_list = get_urn(pattern, df)
            container.append(urn_list)
            del urn_list
        del df
        gc.collect()
    return container


def create_df_for_urn_data_and_save(data: Dict, filename: str) -> None:
    x = pd.DataFrame.from_dict(data, orient="index")
    x.reset_index(inplace=True)
    x.columns = ["urn", "url"]
    x = x[["urn", "url"]]
    path_to_save = Path(f"./data/")
    path_to_save.mkdir(parents=True, exist_ok=True)
    path_to_save = path_to_save / f"{filename}.csv"
    x.to_csv(path_to_save, encoding="utf8", index=False)
