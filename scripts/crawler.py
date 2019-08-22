import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver import firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    StaleElementReferenceException,
    InvalidArgumentException,
)
from typing import List, Dict, Union, Text
import pandas as pd
from loguru import logger
from datetime import datetime
datetime_now = datetime.now().strftime("%Y-%m-%d").replace("-","_")
logger.add(f"./logs/{datetime_now}_file.log")

firefox_webdriver = firefox.webdriver.WebDriver
firefox_webelements = firefox.webelement.FirefoxWebElement

class AcordaosTCU:

    def __init__(self, driver: firefox_webdriver):
        if not isinstance(driver, firefox_webdriver):
            raise TypeError("A classe deve ser iniciada com um webdriver firefox.")
        self.driver = driver
        self.container_of_acordaos = []

    def get_urls(self, years: Union[List[int], int]):
        self.urls = []
        if not isinstance(years, (List, int)):
            raise TypeError("O input precisa ser int ou uma lista.")

        if isinstance(years, List):
            for year in years:
                load_url_data = pd.read_csv(f"./data/tcu_{year}.csv")
                urls = load_url_data["url"].unique().tolist()
                self.urls.extend(urls)
        else:
            load_url_data = pd.read_csv(f"./data/tcu_{years}.csv")
            urls = load_url_data["url"].unique().tolist()
            self.urls.extend(urls)           

    def parse_urls(self):
        for url in self.urls[3482:]:
            self.driver.get(url)
            # localiza no dom o container de "Outras Publicações"
            target_class = "panel-body"
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, target_class))
                )
            except (NoSuchElementException, TimeoutException) as error:
                raise error("Não foi possível localizar os metadados")
            else:
                target_container = self.driver.find_elements_by_class_name(target_class)

            # coleta os links originais do normativo
            filter_elems = self.filter_elements_of_interest(
                target_container, "Tribunal de Contas da União (text/html)"
            )
            if filter_elems:
                if len(filter_elems) > 1:
                    logger.debug("Há mais de um elemento no filtro.")
                for elem in filter_elems:
                    href = elem.find_elements_by_class_name("noprint")[0].get_attribute("href")
                    self.driver.get(href)
                    # identificar se o elemento de ajuda está presente na página
                    pop_up_classname = "body > app-root:nth-child(1) > ajuda:nth-child(3)"
                    try:
                        WebDriverWait(self.driver, 10).until(
                            EC.visibility_of(self.driver.find_element_by_css_selector(pop_up_classname))
                        )
                    except (NoSuchElementException, TimeoutException) as error:
                        # raise error("Não foi possível o popup de ajuda")
                        pass
                    else:
                        elemento_ajuda = self.driver.find_element_by_css_selector(pop_up_classname)
                        # fecha o elemento de ajuda
                        try:
                            WebDriverWait(self.driver, 10).until(
                                EC.invisibility_of_element_located((By.CLASS_NAME, 'tcu-spinner ng-star-inserted'))
                            )
                        except (NoSuchElementException, TimeoutException) as error:
                            raise error()
                        else:
                            try:
                                WebDriverWait(self.driver, 10).until(
                                    EC.visibility_of(self.driver.find_element_by_class_name("modal-close"))
                                )
                            except (NoSuchElementException, TimeoutException) as error:
                                pass
                            else:
                                elemento_ajuda.find_element_by_class_name("modal-close").click()
                        #coleta os dados de interesse
                        dados_acordao = self.coleta_dados_pagina_acordao(self.driver)
                        dados_acordao['url'] = href
                        self.container_of_acordaos.append(dados_acordao)
                        logger.info(f"Finalizado coleta do link {url}.")
            else:
                logger.info("Não há links originais a serem parseados.")
        self.driver.close()

    def to_csv(self, filename: str):
        df = pd.DataFrame(self.container_of_acordaos)
        str_columns = df.select_dtypes('object').columns.tolist()
        for col in str_columns:
            df[col] = df[col].apply(lambda x : x.replace("\n", " ") if x else x)
        df.to_csv(f"{filename}.csv", encoding='utf8', sep=';', index=False)

    @staticmethod
    def filter_elements_of_interest(
        webelements: firefox_webelements, substring: Text
    ) -> Union[List[firefox_webelements], None]:
        if not all(isinstance(elem, firefox_webelements) for elem in webelements):
            raise TypeError(
                "Todos os elementos da lista precisam do tipo FirefoxWebElement"
            )
        str_to_match = substring
        filter_only_elements_of_interest = [
            elem for elem in webelements if str_to_match in elem.text
        ]
        return filter_only_elements_of_interest
    
    @staticmethod
    def coleta_dados_pagina_acordao(browser: firefox_webdriver) -> Dict[str, str]:
        if not isinstance(browser, firefox_webdriver):
            raise TypeError("A função deve receber um firefox webdriver.")
        mapping_dom_id_acordao = {
            "numero_acordao": "conteudo_numero_acordao",
            "relator": "conteudo_relator",
            "processo": "conteudo_processo",
            "tipo_processo": "conteudo_tipo_processo",
            "data_sessao": "conteudo_data_sessao",
            "numero_ata": "conteudo_numero_ata",
            "interessado_reponsavel_recorrente": "conteudo_interessado",
            "entidade": "conteudo_entidade",
            "representante_mp": "conteudo_representante_mp",
            "unidade_tecnica": "conteudo_unidade_tecnica",
            "repr_legal": "conteudo_representante_leval",
            "assunto": "conteudo_assunto",
            "sumario": "conteudo_sumario",
            "acordao": "conteudo_acordao",
            "quorum": "conteudo_quorum",
            "relatorio": "conteudo_relatorio",
            "voto": "conteudo_voto",
        }
        container = {
            "numero_acordao": "",
            "numero_acordao_href": "",
            "relator": "",
            "processo": "",
            "processo_href": "",
            "tipo_processo": "",
            "data_sessao": "",
            "numero_ata": "",
            "numero_ata_href": "",
            "interessado_reponsavel_recorrente": "",
            "entidade": "",
            "representante_mp": "",
            "unidade_tecnica": "",
            "repr_legal": "",
            "assunto": "",
            "sumario": "",
            "acordao": "",
            "quorum": "",
            "relatorio": "",
            "voto": "",
        }
        # coletar dados da página
        ##numero do acordao
        try:
            elem_numero_acordao = browser.find_element_by_id(
                mapping_dom_id_acordao["numero_acordao"]
            )
        except NoSuchElementException:
            container["numero_acordao"] = None
        else:
            container["numero_acordao"] = elem_numero_acordao.text
        ##numero acordao href
        try:
            num_acordao_href = AcordaosTCU.get_a_tag(elem_numero_acordao)
        except (NoSuchElementException, UnboundLocalError):            
            container["numero_acordao_href"] = None
        else:
            if num_acordao_href:
                container["numero_acordao_href"] = num_acordao_href
            else:
                container["numero_acordao_href"] = None
        ##relator
        try:
            elem_relator = browser.find_element_by_id(mapping_dom_id_acordao["relator"]).text
        except NoSuchElementException:
            container["relator"] = None
        else:
            container["relator"] = elem_relator
        ##processo
        try:
            elem_processo = browser.find_element_by_id(mapping_dom_id_acordao["processo"])
        except NoSuchElementException:
            container["processo"] = None
        else:
            container["processo"] = elem_processo.text
        ##processo href
        try:
            processo_href = AcordaosTCU.get_a_tag(elem_processo)
        except (NoSuchElementException, UnboundLocalError):            
            container["processo_href"] = None
        else:
            if processo_href:
                container["processo_href"] = processo_href
            else:
                container["processo_href"] = None
        ##tipo de processo
        try:
            elem_tipo_processo = browser.find_element_by_id(
                mapping_dom_id_acordao["tipo_processo"]
            ).text
        except NoSuchElementException:
            container["tipo_processo"] = None
        else:
            container["tipo_processo"] = elem_tipo_processo
        ##data sessão
        try:
            elem_data_sessao = browser.find_element_by_id(
                mapping_dom_id_acordao["data_sessao"]
            ).text
        except NoSuchElementException:
            container["data_sessao"] = None
        else:
            container["data_sessao"] = elem_data_sessao
        ##numero_da_ata
        try:
            elem_numero_ata = browser.find_element_by_id(mapping_dom_id_acordao["numero_ata"])
        except NoSuchElementException:
            container["numero_ata"] = None
        else:
            container["numero_ata"] = elem_numero_ata.text
        ##numero da ata href
        try:
            numero_ata_href = AcordaosTCU.get_a_tag(elem_numero_ata)
        except (NoSuchElementException, UnboundLocalError):
            container["numero_ata_href"] = None
        else:
            if numero_ata_href:
                container["numero_ata_href"] = numero_ata_href
            else:
                container["numero_ata_href"] = None
        ##interessado
        try:
            elem_interessado = browser.find_element_by_id(
                mapping_dom_id_acordao["interessado_reponsavel_recorrente"]
            ).text
        except NoSuchElementException:
            container["interessado_reponsavel_recorrente"] = None
        else:
            container["interessado_reponsavel_recorrente"] = elem_interessado
        ##entidade
        try:
            elem_entidade = browser.find_element_by_id(mapping_dom_id_acordao["entidade"]).text
        except NoSuchElementException:
            container["entidade"] = None
        else:
            container["entidade"] = elem_entidade
        ##representante_mp
        try:
            elem_repr_mp = browser.find_element_by_id(
                mapping_dom_id_acordao["representante_mp"]
            ).text
        except NoSuchElementException:
            container["representante_mp"] = None
        else:
            container["representante_mp"] = elem_repr_mp
        ##unidade tecnica
        try:
            elem_unidade_tec = browser.find_element_by_id(
                mapping_dom_id_acordao["unidade_tecnica"]
            ).text
        except NoSuchElementException:
            container["unidade_tecnica"] = None
        else:
            container["unidade_tecnica"] = elem_unidade_tec
        ##representante legal
        try:
            elem_repr_legal = browser.find_element_by_id(
                mapping_dom_id_acordao["repr_legal"]
            ).text
        except NoSuchElementException:
            container["repr_legal"] = None
        else:
            container["repr_legal"] = elem_repr_legal
        ##assunto
        try:
            elem_assunto = browser.find_element_by_id(mapping_dom_id_acordao["assunto"]).text
        except NoSuchElementException:
            container["assunto"] = None
        else:
            container["assunto"] = elem_assunto
        ##sumário
        try:
            elem_sumario = browser.find_element_by_id(mapping_dom_id_acordao["sumario"]).text
        except NoSuchElementException:
            container["sumario"] = None
        else:
            container["sumario"] = elem_sumario
        ##acórdão
        try:
            elem_acordao = browser.find_element_by_id(mapping_dom_id_acordao["acordao"]).text
        except NoSuchElementException:
            container["acordao"] = None
        else:
            container["acordao"] = elem_acordao
        ##quorum
        try:
            elem_quorum = browser.find_element_by_id(mapping_dom_id_acordao["quorum"]).text
        except NoSuchElementException:
            container["quorum"] = None
        else:
            container["quorum"] = elem_quorum
        ##relatorio
        try:
            elem_relatorio = browser.find_element_by_id(
                mapping_dom_id_acordao["relatorio"]
            ).text
        except NoSuchElementException:
            container["relatorio"] = None
        else:
            container["relatorio"] = elem_relatorio
        ##voto
        try:
            elem_voto = browser.find_element_by_id(mapping_dom_id_acordao["voto"]).text
        except NoSuchElementException:
            container["voto"] = None
        else:
            container["voto"] = elem_voto

        return container

    @staticmethod
    def get_a_tag(webelement: firefox_webelements) -> Union[Text, None]:
        if not isinstance(webelement, firefox_webelements):
            raise TypeError("O input da função deve ser um firefox webelement.")
        # verifica se há uma a tag presente na hierarquia do webelement
        is_a_tag_present = webelement.find_elements_by_tag_name("a")
        if is_a_tag_present:
            for elem in is_a_tag_present:
                href = elem.get_attribute("href")
                if href:
                    return href
                else:
                    return None
        else:
            return None



