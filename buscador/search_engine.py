import os
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import json


visited_links = set() 
link_to_page = {}
storage_links = []


def load_scores_from_json(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Erro ao carregar pontuações do arquivo JSON: {e}")
        return {}


# Carregar as pontuações do arquivo JSON
scores = load_scores_from_json('pontuacoes.json')


#questao 2.a
def search_links(content, page):
    pontos = 0

    links = BeautifulSoup(content, 'html.parser').find_all('a')

    for link in links:
        href = link.get('href')
        if href:
            if href not in visited_links:
                visited_links[href] = visited_links.get(href, 0) + 1
            if href == page:
                pontos += 20  
            link_to_page[href] = link_to_page.get(href, []) + [page]



def calcular_pontos_para_pagina(page):
    pontos = 0
    for linked_page in link_to_page.get(page, []):
        pontos += 20  
    return pontos


#questao 2.b
termo_pesquisado = input('Sobre o que quer pesquisar? ')
def calcular_pontos_termos(content, termo):
    pontos = 0

    try:
        soup = BeautifulSoup(content, 'html.parser')

        textos = [texto for texto in soup.find_all(string=True, recursive=True) if not (texto.parent.name == '<a>' or (texto.parent.name == '<a>' and texto.parent.get_text(strip=True) == texto))]
        textos += [texto['content'] for texto in soup.find_all('meta', content=True)]  # Adiciona o texto das tags <meta> ao conteúdo
        textos += [texto['content'] for texto in soup.find_all('title', content=True)]  # Adiciona o texto das tags <meta> ao conteúdo

        # Verifica se o termo está presente nos textos e conta as ocorrências
        ocorrencias = sum(texto.lower().count(termo.lower()) for texto in textos)
        # Multiplica o número de ocorrências pelo valor definido para os termos e adiciona ao total de pontos
        pontos += ocorrencias * scores.get('termos')
    except Exception as e:
        print(f"Erro ao calcular pontos pelos termos: {e}")

    return pontos


#questao 2.c
def buscar_ocorrencias_tag(soup, tag_name, termo):
    pontos = 0
    tags_scores = scores['tags']
    tags = soup.find_all(tag_name)
    if tags:
        for tag in tags:
            ocorrencias = tag.get_text().lower().count(termo.lower())
            pontos += ocorrencias * tags_scores.get(tag_name, 0)
    return pontos

def buscar_ocorrencias_title(soup, termo):
    pontos = 0
    tags_scores = scores['tags']
    title_tags = soup.find_all('title')
    if title_tags:
        for tag in title_tags:
            if termo.lower() in tag.get_text().lower():
                pontos += tags_scores.get('title', 0)
    return pontos

def buscar_ocorrencias_meta(soup, termo):
    pontos = 0
    tags_scores = scores['tags']
    meta_tags = soup.find_all('meta')
    if meta_tags:
        for tag in meta_tags:
            if termo.lower() in tag.get('content', '').lower() or termo.lower() in tag.get('name', '').lower():
                pontos += tags_scores.get('meta', 0)
    return pontos

def calcular_pontos_tags(content, termo):
    pontos = 0

    try:
        soup = BeautifulSoup(content, 'html.parser')
        
        if 'tags' in scores:
            pontos += buscar_ocorrencias_title(soup, termo)
            pontos += buscar_ocorrencias_meta(soup, termo)
            pontos += buscar_ocorrencias_tag(soup, 'h1', termo)
            pontos += buscar_ocorrencias_tag(soup, 'h2', termo)
            pontos += buscar_ocorrencias_tag(soup, 'p', termo)
            pontos += buscar_ocorrencias_tag(soup, 'a', termo)
        else:
            print("As pontuações para as tags não foram encontradas no arquivo JSON.")

    except Exception as e:
        print(f"Erro ao calcular pontos pelas tags: {e}")

    return pontos


#questao 2.d 
def calcular_pontos_autoreferencia(page, content):
    pontos = 0

    try:
        soup = BeautifulSoup(content, 'html.parser')
        links = soup.find_all('a', href=lambda href: href == page)

        if links:
            pontos = scores.get('autoreferencia')
    except Exception as e:
        print(f"Erro ao calcular pontos de autoreferência: {e}")

    return pontos


#questao 2.e
def calcular_pontos_frescor(conteudo):
    try:
        soup = BeautifulSoup(conteudo, 'html.parser')
        data_publicacao = soup.find('p', string=lambda text: 'Data da Publicação:' in text or 'Data de postagem:' in text)

        if data_publicacao:
            data_publicacao_texto = data_publicacao.get_text(strip=True)
            ano_publicacao = int(data_publicacao_texto.split('/')[-1])
            ano_atual = datetime.now().year
            diferenca_anos = ano_atual - ano_publicacao

            return 30 - diferenca_anos * 5
        else:
            return 0

    except Exception as e:
        print(f"Erro ao calcular pontos de frescor do conteúdo: {e}")
        return 0


# Função para carregar o conteúdo da página local
def load_content_from_local_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Erro ao carregar conteúdo do arquivo local: {e}")
        return None


# Função para armazenar links encontrados
def armazenar_links(link):
    if link not in storage_links:
        storage_links.append(link)


def main(diretorio='./pages'):
    itens = os.listdir(diretorio)
    arquivos = [item for item in itens if os.path.isfile(os.path.join(diretorio, item))]

    for arquivo in arquivos:
        caminho_completo = os.path.join(diretorio, arquivo)
        conteudo = load_content_from_local_file(caminho_completo)
        if conteudo:
            search_links(conteudo, arquivo)

    resultados = []
    # Calcula os pontos
    for arquivo in arquivos:
        caminho_completo = os.path.join(diretorio, arquivo)
        conteudo = load_content_from_local_file(caminho_completo)
        if conteudo:

            # Calcula os pontos da autoridade - Questão 2.a
            pontos_autoridade = calcular_pontos_para_pagina(arquivo)

            # Calcula os pontos pelo termo - Questão 2.b
            pontos_termos = calcular_pontos_termos(conteudo, termo_pesquisado)

            # Calcula os pontos das tags - Questão 2.c
            pontos_tags = calcular_pontos_tags(conteudo, termo_pesquisado)

            # Calcula os pontos da autoreferência - Questão 2.d
            pontos_autoreferencia = calcular_pontos_autoreferencia(arquivo, conteudo)

            # Calcula os pontos pelo tempo - Questão 2.e
            pontos_frescor = calcular_pontos_frescor(conteudo)

            # Pontos totais
            pontos_totais = pontos_autoridade + pontos_termos + pontos_tags + pontos_autoreferencia + pontos_frescor

            # Deve ser exibida?
            exibicao = "Sim" if pontos_termos > 0 else "Não"

            # Coloca os resultados em uma lista
            resultados.append([arquivo, pontos_autoridade, pontos_termos, pontos_tags, pontos_autoreferencia,
                               pontos_frescor, pontos_totais, exibicao])

    # Questão 03 - Ranqueia os resultados, usando critérios de desempate da lista de resultados
    ranking = sorted(resultados, key=lambda x: (x[6], x[2], x[5], x[1]), reverse=True)

    # Questão 07 - Criação da planilha com os resultados
    planilha = pd.DataFrame(ranking, columns=['Pagina', 
                                              'Autoridade', 
                                              'Frequencia dos termos', 
                                              'Uso em tags',
                                              'Autoreferencia', 
                                              'Frescor do conteudo', 
                                              'Total',  
                                              'Deve ser exibida'
                                              ])
    planilha.to_excel('resultados.xlsx', index=False)
    print("Planilha com os resultados salvos em 'resultados.xlsx'")

    # Imprime os links armazenados
    print("\nLinks armazenados:")
    for link in storage_links:
        print(link)

    # Baixa e processa as páginas referenciadas
    for link in storage_links:
        print(f"\nProcessando página referenciada: {link}")
        conteudo_referenciado = load_content_from_local_file(os.path.join(diretorio, link))
        if conteudo_referenciado:
            search_links(conteudo_referenciado, link)


main()
