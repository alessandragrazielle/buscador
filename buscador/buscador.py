import requests
from bs4 import BeautifulSoup
import os



visited_links = {}


def searchLinks(content, page):
    pontos = 0

    links = BeautifulSoup(content, 'html.parser')
    countLinks = links.find_all('a')

    for link in countLinks:
        href = link['href']
        if href and href not in visited_links:
            visited_links[href] = visited_links.get(href, 0) + 1
        pontos += 20

    print(f'A página {page} recebeu {pontos} pontos')
    


def ler_arquivos_pasta(diretorio = './pages'):
    # Lista todos os arquivos e diretórios no diretório especificado
    itens = os.listdir(diretorio)
    
    # Filtra apenas os arquivos
    arquivos = [item for item in itens if os.path.isfile(os.path.join(diretorio, item))]
    
    # Para cada arquivo, abre e lê seu conteúdo
    for arquivo in arquivos:
        caminho_completo = os.path.join(diretorio, arquivo)
        with open(caminho_completo, 'r', encoding='utf-8') as f:
            conteudo = f.read()
            searchLinks(conteudo, arquivo)
ler_arquivos_pasta()



def searchTerm(url, termo):
    with open(url, 'r', encoding='utf-8') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'html.parser')
        countTerms = soup.find_all(termo)

        for i in countTerms:
            pontos += 5
    
    print('Este site fez', pontos, 'pontos')




