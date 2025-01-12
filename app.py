from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass
from utils import extrair_dados, contar_pontos

##estou sentindo uma vibe estranha

@dataclass
class ArquivoTXT:
    nome: str
    caminho: Path

class ProcessadorArquivos:
    def __init__(self, diretorio: Path = Path('.')):
        self.diretorio = diretorio

    def listar_arquivos_txt(self) -> List[ArquivoTXT]:
        return [
            ArquivoTXT(arquivo.name, arquivo)
            for arquivo in self.diretorio.glob('*.txt')
        ]

    def processar_arquivo(self, arquivo: ArquivoTXT) -> None:
        try:
            with arquivo.caminho.open('r', encoding='utf-8') as file:
                for linha in map(str.strip, file):
                    if linha:
                        dados = extrair_dados(linha)
                        print(dados)
        except Exception as e:
            print(f'Erro ao processar arquivo {arquivo.nome}: {str(e)}')

class MenuInterativo:
    def __init__(self):
        self.processador = ProcessadorArquivos()

    def exibir(self) -> None:
        while True:
            if not self._mostrar_opcoes():
                break
            
            if opcao := self._obter_escolha():
                self.processador.processar_arquivo(opcao)

    def _mostrar_opcoes(self) -> bool:
        arquivos = self.processador.listar_arquivos_txt()
        
        print('\n=== Menu de Arquivos TXT ===')
        
        if not arquivos:
            print('Nenhum arquivo .txt encontrado na pasta!')
            return False
        
        for i, arquivo in enumerate(arquivos, 1):
            print(f'{i}. {arquivo.nome}')
        print('0. Sair')
        
        return True

    def _obter_escolha(self) -> Optional[ArquivoTXT]:
        arquivos = self.processador.listar_arquivos_txt()
        try:
            escolha = int(input('\nEscolha um arquivo (0 para sair): '))
            
            if escolha == 0:
                return None
            if 1 <= escolha <= len(arquivos):
                return arquivos[escolha - 1]
            
            print('\nOpção inválida!')
        except ValueError:
            print('\nPor favor, digite um número válido!')
        return None

def main():
    try:
        menu = MenuInterativo()
        menu.exibir()
    except KeyboardInterrupt:
        print('\nPrograma encerrado pelo usuário')
    except Exception as e:
        print(f'Erro inesperado: {str(e)}')

if __name__ == '__main__':
    main()