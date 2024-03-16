import os
from bs4 import BeautifulSoup



visited_pages = {}

def search_term(content, termo, page):
    pontos = 0

    soup = BeautifulSoup(termo, 'html.parser')
    ocorrencias = soup.get_text()
    terms = ocorrencias.split()
    term_count = terms.count(termo)
    if page not in visited_pages:
        visited_pages[page] = True

        if term_count > 0:
            pontos += term_count * 5
            print('Este site fez', pontos, 'pontos')
            print(f'O termo {termo} aparece {term_count} vezes na página {page}')
        else:
            print(f'O termo {termo} não ')


def ler_arquivos_pasta(diretorio='./pages'):
    itens = os.listdir(diretorio)
    arquivos = [item for item in itens if os.path.isfile(os.path.join(diretorio, item))]
    for arquivo in arquivos:
        caminho_completo = os.path.join(diretorio, arquivo)
        with open(caminho_completo, 'r', encoding='utf-8') as f:
            conteudo = f.read()
            search_term(conteudo, 'Links', arquivo)

ler_arquivos_pasta()
