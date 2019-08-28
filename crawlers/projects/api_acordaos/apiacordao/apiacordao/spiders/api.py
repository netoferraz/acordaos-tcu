# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import json
from ..items import AcordaoItem
import re
import json
from datetime import datetime


class ApiSpider(scrapy.Spider):
    name = "api"

    def start_requests(self):
        with open("../../../../data/api/parsed/2009.json", "r") as _:
            container = json.load(_)
            for data in container:
                urn = data["urn"]
                url = data["url"]
                yield Request(url, cb_kwargs=dict(urn=urn))

    def parse(self, response, urn):
        res = json.loads(response.body, encoding="utf8")
        res = res["documentos"][0]
        data = AcordaoItem()
        data["urn"] = urn
        data["urn_year"] = re.search("\d{4}-\d{2}-\d{2}", urn).group(0)[:4]
        data["numero_acordao"] = self.clean_text(res["NUMACORDAO"])
        data["numero_acordao_href"] = res["URLARQUIVO"].strip()
        data["relator"] = self.clean_text(res["RELATOR"])
        data["processo"] = self.clean_text(self.remove_tags_html(res["PROC"]))
        data["processo_href"] = res["URLARQUIVO"]
        data["tipo_processo"] = self.clean_text(res["ASSUNTO"])
        data["data_sessao"] = self.clean_text(res["DATASESSAO"])
        data["numero_ata"] = self.clean_text(f"{res['NUMATA']}-{res['COLEGIADO']}")
        data["interessado_reponsavel_recorrente"] = self.clean_text(
            self.remove_tags_html(res["INTERESSADOS"])
        )
        data["entidade"] = self.clean_text(res["ENTIDADE"])
        data["representante_mp"] = self.clean_text(res["REPRESENTANTEMP"])
        data["unidade_tecnica"] = self.clean_text(res["UNIDADETECNICA"])
        data["repr_legal"] = self.clean_text(res["ADVOGADO"])
        data["assunto"] = self.clean_text(res["ASSUNTO"])
        data["sumario"] = self.clean_text(res["SUMARIO"])
        data["acordao"] = self.clean_text(self.remove_tags_html(res["ACORDAO"]))
        data["quorum"] = self.clean_text(self.remove_tags_html(res["QUORUM"]))
        data["relatorio"] = self.clean_text(self.remove_tags_html(res["RELATORIO"]))
        data["voto"] = self.clean_text(self.remove_tags_html(res["VOTO"]))
        data["was_downloaded"] = 1
        data["downloaded_at"] = datetime.now().strftime("%Y-%m-%d")
        yield data

    def remove_tags_html(self, texto: str) -> str:
        cleanr = re.compile("<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")
        cleantext = re.sub(cleanr, "", texto)
        return cleantext.replace("\t", " ").replace("\n", " ").strip()

    def clean_text(self, texto: str) -> str:
        texto = texto.replace("\xa0", "").replace("\t", " ").replace("\n", " ").strip()
        return texto
