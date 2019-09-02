# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AcordaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    urn = scrapy.Field()
    url_lexml = scrapy.Field() 
    urn_year = scrapy.Field() 
    numero_acordao = scrapy.Field() 
    numero_acordao_href = scrapy.Field() 
    relator = scrapy.Field() 
    processo = scrapy.Field()
    processo_href = scrapy.Field() 
    tipo_processo = scrapy.Field() 
    data_sessao = scrapy.Field() 
    numero_ata = scrapy.Field() 
    numero_ata_href = scrapy.Field() 
    interessado_reponsavel_recorrente = scrapy.Field() 
    entidade = scrapy.Field() 
    representante_mp = scrapy.Field() 
    unidade_tecnica = scrapy.Field() 
    repr_legal = scrapy.Field() 
    assunto = scrapy.Field() 
    sumario = scrapy.Field()
    acordao = scrapy.Field() 
    quorum = scrapy.Field() 
    relatorio = scrapy.Field() 
    voto = scrapy.Field() 
    url_tcu = scrapy.Field() 
    was_downloaded = scrapy.Field()
    downloaded_at = scrapy.Field() 
