import os
import pandas as pd
import json
from search_engine import Buscador

def carregar_scores_do_json(caminho_json):
    """Carrega os scores de um arquivo JSON."""
    if os.path.exists(caminho_json):
        with open(caminho_json, 'r') as file:
            return json.load(file)
    else:
        return {}

def salvar_scores_para_json(scores, caminho_json):
    """Salva os scores em um arquivo JSON."""
    with open(caminho_json, 'w') as file:
        json.dump(scores, file, indent=4)

def editar_scores(scores):
    """Permite ao usuário editar os scores."""
    print("Scores atuais:")
    print(scores)
    while True:
        chave = input("Digite o nome do critério de pontuação que deseja editar (ou deixe em branco para sair): ").strip()
        if not chave:
            break
        if chave in scores:
            novo_valor = input(f"Digite o novo valor para '{chave}': ").strip()
            if isinstance(scores[chave], dict):
                # Se for um dicionário, precisamos editar subchaves
                print(f"Subcategorias para '{chave}':")
                print(scores[chave])
                subchave = input("Digite o nome da subcategoria que deseja editar: ").strip()
                if subchave in scores[chave]:
                    novo_valor_subchave = input(f"Digite o novo valor para '{subchave}': ").strip()
                    scores[chave][subchave] = float(novo_valor_subchave)
                    print(f"Valor para '{subchave}' atualizado.")
                else:
                    print("Subchave não encontrada.")
            else:
                scores[chave] = float(novo_valor)
                print(f"Valor para '{chave}' atualizado.")
        else:
            print("Chave não encontrada nos scores.")

def main(diretorio='./pages', caminho_json_scores='./pontuacoes.json'):
    buscador = Buscador()

    itens = os.listdir(diretorio)
    arquivos = [item for item in itens if os.path.isfile(os.path.join(diretorio, item))]

    for arquivo in arquivos:
        caminho_completo = os.path.join(diretorio, arquivo)
        conteudo = buscador.load_content_from_local_file(caminho_completo)
        if conteudo:
            buscador.search_links(conteudo, arquivo)

    resultados = []
    # Calcula os pontos
    for arquivo in arquivos:
        caminho_completo = os.path.join(diretorio, arquivo)
        conteudo = buscador.load_content_from_local_file(caminho_completo)
        if conteudo:

            # Calcula os pontos da autoridade - Questão 2.a
            pontos_autoridade = buscador.calcular_pontos_para_pagina(arquivo)

            # Calcula os pontos pelo termo - Questão 2.b
            pontos_termos = buscador.calcular_pontos_termos(conteudo, termo_pesquisado)

            # Calcula os pontos das tags - Questão 2.c
            pontos_tags = buscador.calcular_pontos_tags(conteudo, termo_pesquisado)

            # Calcula os pontos da autoreferência - Questão 2.d
            pontos_autoreferencia = buscador.calcular_pontos_autoreferencia(arquivo, conteudo)

            # Calcula os pontos pelo tempo - Questão 2.e
            pontos_frescor = buscador.calcular_pontos_frescor(conteudo)

            # Pontos totais
            pontos_totais = (
                pontos_autoridade +
                pontos_termos +
                pontos_tags +
                pontos_autoreferencia +
                pontos_frescor
            )

            # Deve ser exibida?
            exibicao = "Sim" if pontos_termos > 0 else "Não"

            # Coloca os resultados em uma lista 
            resultados.append([
                arquivo, 
                pontos_autoridade, 
                pontos_termos, 
                pontos_tags, 
                pontos_autoreferencia,
                pontos_frescor, 
                pontos_totais, 
                exibicao
            ])

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

    # Criando arquivo HTML com a planilha
    with open('resultados.html', 'w') as f:
        f.write(planilha.to_html())

    # Imprime os links armazenados
    print("\nLinks armazenados:")
    for link in buscador.storage_links:
        print(link)

    # Baixa e processa as páginas referenciadas
    for link in buscador.storage_links:
        print(f"\nProcessando página referenciada: {link}")
        conteudo_referenciado = buscador.load_content_from_local_file(os.path.join(diretorio, link))
        if conteudo_referenciado:
            buscador.search_links(conteudo_referenciado, link)

    # Adiciona a opção de editar os scores
    scores = carregar_scores_do_json(caminho_json_scores)
    editar_scores(scores)
    salvar_scores_para_json(scores, caminho_json_scores)

if __name__ == "__main__":
    termo_pesquisado = input('Sobre o que quer pesquisar? ')
    main()
