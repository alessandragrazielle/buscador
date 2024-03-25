import json

def load_scores_from_json(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Erro ao carregar pontuações do arquivo JSON: {e}")
        return {}


def save_scores_to_json(scores, file_path):
    try:
        with open(file_path, 'w') as f:
            json.dump(scores, f, indent=4)
            print("Pontuações atualizadas com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar pontuações no arquivo JSON: {e}")


def edit_scores():
    file_path = 'pontuacoes.json'
    scores = load_scores_from_json(file_path)

    print("Pontuações atuais:")
    print(json.dumps(scores, indent=4))

    while True:
        termo = input("Digite o termo que deseja editar (ou 'sair' para encerrar): ").strip()
        if termo.lower() == 'sair':
            break
        if termo not in scores:
            print("Termo não encontrado nas pontuações.")
            continue
        novo_score = input(f"Digite o novo score para '{termo}': ").strip()
        try:
            novo_score = float(novo_score)
            scores[termo] = novo_score
            save_scores_to_json(scores, file_path)
        except ValueError:
            print("Valor inválido. Por favor, insira um número.")

if __name__ == "__main__":
    edit_scores()
