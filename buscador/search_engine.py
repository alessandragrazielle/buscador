import os
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd


visited_links = {}
link_to_page = {}


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

    soup = BeautifulSoup(content, 'html.parser') 
    
    pontos += len(soup.find_all(string = lambda text: termo_pesquisado.lower() in text.lower())) * 5
     
    return pontos


#questao 2.c
def calcular_pontos_tags(content):
    pontos = 0
    soup = BeautifulSoup(content, 'html.parser')
  
    pontos += len(soup.find_all('h1')) * 20
    pontos += len(soup.find_all('h2')) * 10
    pontos += len(soup.find_all('p')) * 5
    pontos += len(soup.find_all('a')) * 2

    return pontos


#questao 2.d (FALTA FAZER)
def calcular_pontos_autoreferencia():
    pontos = 0

    return pontos


#questao 2.e
def calcular_pontos_frescor(conteudo):
    pontos = 0
    soup = BeautifulSoup(conteudo, 'html.parser')

    data_publicacao = soup.find('p', string=lambda text: 'Data da Publicação:' in text or 'Data de postagem:' in text)
    
    if data_publicacao:
        data_publicacao_texto = data_publicacao.get_text(strip=True)
        ano_publicacao = int(data_publicacao_texto.split('/')[-1])
        ano_atual = datetime.now().year
    
        diferenca_anos = ano_atual - ano_publicacao
        pontos = 30 - diferenca_anos * 5
        
        return pontos


def ler_arquivos_pasta(diretorio='./pages'):
    itens = os.listdir(diretorio)
    arquivos = [item for item in itens if os.path.isfile(os.path.join(diretorio, item))]

    for arquivo in arquivos:
        caminho_completo = os.path.join(diretorio, arquivo)
        with open(caminho_completo, 'r', encoding='utf-8') as f:
            conteudo = f.read()
            search_links(conteudo, arquivo)

    
    resultados = []
    #calcula os pontos
    for arquivo in arquivos:
        caminho_completo = os.path.join(diretorio, arquivo)
        with open(caminho_completo, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
            #calcula os pontos da autoridade - questao 2.a
            pontos_autoridade = calcular_pontos_para_pagina(arquivo)
            #print(f'A página {arquivo} recebeu {pontos} pontos')

            #calcula os pontos pelo termo - questao 2.b
            pontos_termos = calcular_pontos_termos(conteudo, termo_pesquisado)
            #print(f'A página {arquivo} recebeu {pontos_termos} pontos pela quantidade de TERMOS')

            #calcula os pontos das tags - questao 2.c
            pontos_tags = calcular_pontos_tags(conteudo)
            #print(f'A página {arquivo} recebeu {pontos_tags} pontos pelo USO EM TAGS')

            #calcula os pontos da autoreferencia - questao 2.d
            pontos_autoreferencia = calcular_pontos_autoreferencia()

            #calcula os pontos pelo tempo - questao 2.e
            pontos_frescor = calcular_pontos_frescor(conteudo)
            #print(f'A página {arquivo} recebeu {pontos_frescor} pontos pelo FRESCOR DO CONTEUDO \n')

            #pontos totais
            pontos_totais = pontos_autoridade + pontos_termos + pontos_tags + pontos_frescor

            #deve ser exibida?
            exibicao = ''
            if(pontos_termos > 0): exibicao = "Sim"
            else: exibicao = 'Não'

            #coloca os resultados em uma lista
            resultados.append([arquivo, pontos_autoridade, pontos_termos, pontos_tags, pontos_autoreferencia, pontos_frescor, pontos_totais, exibicao])

    
    #questao 03 - ranqueia os resultados, usando criterios de desempate da lista de resultados
    ranking = sorted(resultados, key = lambda x: (x[6], x[2], x[5], x[1]), reverse=True) 
    
    #questao 07 - criacao da planilha com os resultados
    planilha = pd.DataFrame(ranking, columns=['Pagina', 'Autoridade', 'Frequencia dos termos', 'Uso em tags', 'Autoreferencia', 'Frescor do conteudo', 'Total', 'Deve ser exibida'])
    planilha.to_excel('resultados.xlsx', index=False)
    print("Planilha com os resultados salvos em 'resultados.xlsx'")
    

ler_arquivos_pasta()
