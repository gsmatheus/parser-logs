import os
from utils import extrair_dados, contar_pontos

def listar_arquivos_txt():
    arquivos = [f for f in os.listdir('.') if f.endswith('.txt')]
    return arquivos

def exibir_menu():
    while True:
        arquivos = listar_arquivos_txt()
        print("\n=== Menu de Arquivos TXT ===")
        
        if not arquivos:
            print("Nenhum arquivo .txt encontrado na pasta!")
            return
        
        for i, arquivo in enumerate(arquivos, 1):
            print(f"{i}. {arquivo}")
        
        print("0. Sair")
        
        try:
            escolha = int(input("\nEscolha um arquivo (0 para sair): "))
            
            if escolha == 0:
                break
            elif 1 <= escolha <= len(arquivos):
                arquivo_selecionado = arquivos[escolha - 1]
                print(arquivo_selecionado)
                percorrer_arquivo(arquivo_selecionado)
            else:
                print("\nOpção inválida!")
        except ValueError:
            print("\nPor favor, digite um número válido!")

def percorrer_arquivo(arquivo):
    with open(arquivo, 'r') as file:
        for linha in file:
            linha = linha.strip()
            
            dados = extrair_dados(linha)
            print(dados)

if __name__ == "__main__":
    exibir_menu()