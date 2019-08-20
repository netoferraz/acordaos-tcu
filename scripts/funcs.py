import os
import pandas as pd
import json
import re
import gc
from typing import List, Dict, Union, Text
from numbers import Number
from pathlib import Path
import selenium
firefox_webelements = selenium.webdriver.firefox.webelement.FirefoxWebElement
firefox_webdriver = selenium.webdriver.firefox.webdriver.WebDriver
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

def filter_elements_of_interest(webelements: firefox_webelements, substring: Text) -> Union[List[firefox_webelements], None]:
    if not all(isinstance(elem, firefox_webelements) for elem in webelements):
        raise TypeError("Todos os elementos da lista precisam do tipo FirefoxWebElement")
    str_to_match = substring
    filter_only_elements_of_interest = [elem for elem in webelements if str_to_match in elem.text]
    return filter_only_elements_of_interest

def get_a_tag(webelement: firefox_webelements) -> Union[Text, None]:
    if not isinstance(webelement, firefox_webelements):
        raise TypeError("O input da função deve ser um firefox webelement.")
    #verifica se há uma a tag presente na hierarquia do webelement
    is_a_tag_present = webelement.find_elements_by_tag_name('a')
    if is_a_tag_present:
        for elem in is_a_tag_present:
            href = elem.get_attribute('href')
            if href:
                return href
            else:
                return None
    else:
        return None

def coleta_dados_pagina_acordao(browser: firefox_webdriver) -> Dict[str,str]:
    if not isinstance(browser, firefox_webdriver):
        raise TypeError("A função deve receber um firefox webdriver.")
    mapping_dom_id_acordao = {
        'numero_acordao' : "conteudo_numero_acordao",
        'relator' : "conteudo_relator",
        'processo' : "conteudo_processo",
        'tipo_processo' : "conteudo_tipo_processo",
        'data_sessao' : "conteudo_data_sessao",
        'numero_ata' : "conteudo_numero_ata",
        'interessado_reponsavel_recorrente' : 'conteudo_interessado',
        'entidade' : 'conteudo_entidade',
        'representante_mp' : 'conteudo_representante_mp',
        'unidade_tecnica' : 'conteudo_unidade_tecnica',
        'repr_legal' : 'conteudo_representante_leval',
        'assunto' : 'conteudo_assunto',
        'sumario' : 'conteudo_sumario',
        'acordao' : 'conteudo_acordao',
        'quorum' : 'conteudo_quorum',
        'relatorio' : 'conteudo_relatorio',
        'voto' : 'conteudo_voto'
    }
    container = {
        'numero_acordao' : "",
        'numero_acordao_href' : "",
        'relator' : "",
        'processo' : "",
        'processo_href' : "",
        'tipo_processo' : "",
        'data_sessao' : "",
        'numero_ata' : "",
        'numero_ata_href' : "",
        'interessado_reponsavel_recorrente' : '',
        'entidade' : '',
        'representante_mp' : '',
        'unidade_tecnica' : '',
        'repr_legal' : '',
        'assunto' : '',
        'sumario' : '',
        'acordao' : '',
        'quorum' : '',
        'relatorio' : '',
        'voto' : ''
    }
    #coletar dados da página
    ##numero do acordao
    elem_numero_acordao = browser.find_element_by_id(mapping_dom_id_acordao['numero_acordao'])
    container['numero_acordao'] = elem_numero_acordao.text
    ##numero acordao href
    num_acordao_href =  get_a_tag(elem_numero_acordao)
    if num_acordao_href:
        container['numero_acordao_href'] = num_acordao_href
    ##relator
    elem_relator = browser.find_element_by_id(mapping_dom_id_acordao['relator']).text
    container['relator'] = elem_relator
    ##processo
    elem_processo = browser.find_element_by_id(mapping_dom_id_acordao['processo'])
    container['processo'] = elem_processo.text
    ##processo href
    processo_href =  get_a_tag(elem_processo)
    if processo_href:
        container['processo_href'] = processo_href
    ##tipo de processo
    elem_tipo_processo = browser.find_element_by_id(mapping_dom_id_acordao['tipo_processo']).text
    container['tipo_processo'] = elem_tipo_processo
    ##data sessão
    elem_data_sessao = browser.find_element_by_id(mapping_dom_id_acordao['data_sessao']).text
    container['data_sessao'] = elem_data_sessao
    ##numero_da_ata
    elem_numero_ata = browser.find_element_by_id(mapping_dom_id_acordao['numero_ata'])
    container['numero_ata'] = elem_numero_ata.text
    ##numero da ata href
    numero_ata_href =  get_a_tag(elem_numero_ata)
    if numero_ata_href:
        container['numero_ata_href'] = numero_ata_href
    ##interessado
    elem_interessado = browser.find_element_by_id(mapping_dom_id_acordao['interessado_reponsavel_recorrente']).text
    container['interessado_reponsavel_recorrente'] = elem_interessado
    ##entidade
    elem_entidade = browser.find_element_by_id(mapping_dom_id_acordao['entidade']).text
    container['entidade'] = elem_entidade
    ##representante_mp
    elem_repr_mp = browser.find_element_by_id(mapping_dom_id_acordao['representante_mp']).text
    container['representante_mp'] = elem_repr_mp
    ##unidade tecnica
    elem_unidade_tec = browser.find_element_by_id(mapping_dom_id_acordao['unidade_tecnica']).text
    container['unidade_tecnica'] = elem_unidade_tec
    ##representante legal
    elem_repr_legal = browser.find_element_by_id(mapping_dom_id_acordao['repr_legal']).text
    container['repr_legal'] = elem_repr_legal
    ##assunto
    elem_assunto = browser.find_element_by_id(mapping_dom_id_acordao['assunto']).text
    container['assunto'] = elem_assunto
    ##sumário
    elem_sumario = browser.find_element_by_id(mapping_dom_id_acordao['sumario']).text
    container['sumario'] = elem_sumario
    ##acórdão
    elem_acordao = browser.find_element_by_id(mapping_dom_id_acordao['acordao']).text
    container['acordao'] = elem_acordao
    ##quorum
    elem_quorum = browser.find_element_by_id(mapping_dom_id_acordao['quorum']).text
    container['quorum'] = elem_quorum
    ##relatorio
    elem_relatorio = browser.find_element_by_id(mapping_dom_id_acordao['relatorio']).text
    container['relatorio'] = elem_relatorio
    ##voto
    elem_voto = browser.find_element_by_id(mapping_dom_id_acordao['voto']).text
    container['voto'] = elem_voto
    
    return container




    

