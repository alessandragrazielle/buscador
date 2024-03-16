import os
from bs4 import BeautifulSoup


visited_links = {}
link_to_page = {}


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


def ler_arquivos_pasta(diretorio='./pages'):
    itens = os.listdir(diretorio)
    arquivos = [item for item in itens if os.path.isfile(os.path.join(diretorio, item))]

    for arquivo in arquivos:
        caminho_completo = os.path.join(diretorio, arquivo)
        with open(caminho_completo, 'r', encoding='utf-8') as f:
            conteudo = f.read()
            search_links(conteudo, arquivo)

    for arquivo in arquivos:
        pontos = calcular_pontos_para_pagina(arquivo)
        print(f'A página {arquivo} recebeu {pontos} pontos')


ler_arquivos_pasta()

def search_term(path, termo):
    pontos = 0

    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'html.parser')
        count_terms = soup.find_all(termo)

        pontos += len(count_terms) * 5

    print('Este site fez', pontos, 'pontos')

