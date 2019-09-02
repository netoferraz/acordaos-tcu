# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3 as sql


class ApiacordaoPipeline(object):
    def __init__(self):
        self.create_cnx()

    def create_cnx(self):
        self.conn = sql.connect("../../../../db/acordaos-download.db")
        self.cursor = self.conn.cursor()

    def store_db(self, item):
        query_string = f"""
        UPDATE download_acordaos 
        SET urn_year = {item['urn_year']}, 
        numero_acordao = '{item['numero_acordao']}', 
        numero_acordao_href = '{item['numero_acordao_href']}',
        relator = '{item['relator']}',
        processo = '{item['processo']}',
        processo_href = '{item['processo_href']}',
        tipo_processo = '{item['tipo_processo']}',
        data_sessao = '{item['data_sessao']}',
        numero_ata = '{item['numero_ata']}',
        interessado_reponsavel_recorrente = '{item['interessado_reponsavel_recorrente']}',
        entidade = '{item['entidade']}',
        representante_mp = '{item['representante_mp']}',
        unidade_tecnica = '{item['unidade_tecnica']}',
        repr_legal = '{item['repr_legal']}',
        assunto = '{item['assunto']}',
        sumario = '{item['sumario']}',
        acordao = '{item['acordao']}',
        quorum = '{item['quorum']}',
        relatorio = '{item['relatorio']}',
        voto = '{item['voto']}',
        was_downloaded = {item['was_downloaded']},
        downloaded_at = {item['downloaded_at']}
        WHERE urn = '{item['urn']}'"""
        self.cursor.execute(query_string)
        self.conn.commit()

    def process_item(self, item, spider):
        self.store_db(item)
        return item
