import os
from bs4 import BeautifulSoup



def search_term(content, termo):
    pontos = 0

    soup = BeautifulSoup(content, 'html.parser')
    count_terms = soup.find_all(termo)

    pontos += len(count_terms) * 5

    print('Este site fez', pontos, 'pontos')
    print(f'O termo {termo} aparece {len(count_terms)} vezes na página')




def ler_arquivos_pasta(diretorio='./pages'):
    itens = os.listdir(diretorio)
    arquivos = [item for item in itens if os.path.isfile(os.path.join(diretorio, item))]

    for arquivo in arquivos:
        caminho_completo = os.path.join(diretorio, arquivo)
        with open(caminho_completo, 'r', encoding='utf-8') as f:
            conteudo = f.read()
            search_term(conteudo, 'Links')

ler_arquivos_pasta()
