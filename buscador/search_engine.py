import os
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import json


class Buscador:
    def __init__(self):
        self.visited_links = set()  
        self.link_to_page = {}
        self.storage_links = []
        self.scores = self.load_scores_from_json('pontuacoes.json')

    def load_scores_from_json(self, file_path):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar pontuações do arquivo JSON: {e}")
            return {}

    def search_links(self, content, page):
        pontos = 0

        links = BeautifulSoup(content, 'html.parser').find_all('a')

        for link in links:
            href = link.get('href')
            if href:
                if href not in self.visited_links:
                    self.visited_links.add(href)
                    self.armazenar_links(href)
                if href == page:
                    pontos += self.scores.get('autoridade')
                self.link_to_page[href] = self.link_to_page.get(href, []) + [page]

    def calcular_pontos_para_pagina(self, page):
        pontos = 0
        for linked_page in self.link_to_page.get(page, []):
            pontos += self.scores.get('autoridade')
        return pontos

    def calcular_pontos_termos(self, content, termo):
        pontos = 0

        try:
            soup = BeautifulSoup(content, 'html.parser')
            # Encontra todo o conteúdo de texto dentro do HTML, incluindo o texto das tags <title> e <meta>, mas excluindo as ocorrências dentro das tags <script>, <style> e <a>
            textos = [texto for texto in soup.find_all(string=True, recursive=True) if not (texto.parent.name == '<a>' or (texto.parent.name == '<a>' and texto.parent.get_text(strip=True) == texto))]
            textos += [texto['content'] for texto in soup.find_all('meta', content=True)]  # Adiciona o texto das tags <meta> ao conteúdo
            textos += [texto['content'] for texto in soup.find_all('title', content=True)]  # Adiciona o texto das tags <meta> ao conteúdo

            # Verifica se o termo está presente nos textos e conta as ocorrências
            ocorrencias = sum(texto.lower().count(termo.lower()) for texto in textos)
            # Multiplica o número de ocorrências pelo valor definido para os termos e adiciona ao total de pontos
            pontos += ocorrencias * self.scores.get('termos')
        except Exception as e:
            print(f"Erro ao calcular pontos pelos termos: {e}")

        return pontos

    def buscar_ocorrencias_title(self, soup, termo):
        pontos = 0
        tags_scores = self.scores['tags']
        title_tags = soup.find_all('title')
        if title_tags:
            for tag in title_tags:
                if termo.lower() in tag.get_text().lower():
                    pontos += tags_scores.get('title', 0)
        return pontos

    def buscar_ocorrencias_meta(self, soup, termo):
        pontos = 0
        tags_scores = self.scores['tags']
        meta_tags = soup.find_all('meta')
        if meta_tags:
            for tag in meta_tags:
                if termo.lower() in tag.get('content', '').lower() or termo.lower() in tag.get('name', '').lower():
                    pontos += tags_scores.get('meta', 0)
        return pontos

    def buscar_ocorrencias_tag(self, soup, tag_name, termo):
        pontos = 0
        tags_scores = self.scores.get('tags', {})
        tag_score = tags_scores.get(tag_name, 0)

        tags = soup.find_all(tag_name)
        if tags:
            for tag in tags:
                ocorrencias = tag.get_text().lower().count(termo.lower())
                pontos += ocorrencias * tag_score

        return pontos

    def calcular_pontos_tags(self, content, termo):
        pontos = 0

        try:
            soup = BeautifulSoup(content, 'html.parser')

            if 'tags' in self.scores:
                # Busca ocorrências em cada tipo de tag e adiciona os pontos correspondentes
                pontos += self.buscar_ocorrencias_title(soup, termo)
                pontos += self.buscar_ocorrencias_meta(soup, termo)
                pontos += self.buscar_ocorrencias_tag(soup, 'h1', termo)
                pontos += self.buscar_ocorrencias_tag(soup, 'h2', termo)
                pontos += self.buscar_ocorrencias_tag(soup, 'p', termo)
                pontos += self.buscar_ocorrencias_tag(soup, 'a', termo)
            else:
                print("As pontuações para as tags não foram encontradas no arquivo JSON.")

        except Exception as e:
            print(f"Erro ao calcular pontos pelas tags: {e}")

        return pontos

    def calcular_pontos_autoreferencia(self, page, content):
        pontos = 0

        try:
            soup = BeautifulSoup(content, 'html.parser')
            links = soup.find_all('a', href=lambda href: href == page)

            if links:
                pontos = self.scores.get('autoreferencia')
        except Exception as e:
            print(f"Erro ao calcular pontos de autoreferência: {e}")

        return pontos

    def calcular_pontos_frescor(self, conteudo):
        try:
            soup = BeautifulSoup(conteudo, 'html.parser')
            data_publicacao = soup.find('p', string=lambda text: 'Data da Publicação:' in text or 'Data de postagem:' in text)

            if data_publicacao:
                data_publicacao_texto = data_publicacao.get_text(strip=True)
                ano_publicacao = int(data_publicacao_texto.split('/')[-1])
                ano_atual = datetime.now().year

                diferenca_anos = ano_atual - ano_publicacao

                return 30 - (diferenca_anos * 5)
            
            else:
                return 0

        except Exception as e:
            print(f"Erro ao calcular pontos de frescor do conteúdo: {e}")
            return 0

    def load_content_from_local_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Erro ao carregar conteúdo do arquivo local: {e}")
            return None

    def armazenar_links(self, link):
        if link not in self.storage_links:
            self
