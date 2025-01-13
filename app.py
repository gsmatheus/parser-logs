from datetime import datetime
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass
from utils import extrair_dados, gera_hash, info, erro, sucesso
from mongodb_manager import MongoDBManager

@dataclass
class ArquivoTXT:
    nome: str
    caminho: Path

class ProcessadorArquivos:
    def __init__(self, diretorio: Path = Path('.')):
        self.diretorio = diretorio
        self.mongodb_manager = MongoDBManager()
        self.mongodb_manager.criar_collection_credenciais()
        
    def listar_arquivos_txt(self) -> List[ArquivoTXT]:
        return [
            ArquivoTXT(arquivo.name, arquivo)
            for arquivo in self.diretorio.glob('*.txt')
        ]

    def processar_arquivo(self, arquivo: ArquivoTXT) -> None:
        try:
            with arquivo.caminho.open('r', encoding='utf-8') as file:
                count = 10000
                batch = []
                for linha in map(str.strip, file):
                    if linha:
                        try:
                            dados = extrair_dados(linha)
                            hash = gera_hash(str(dados))                        
                            dados['hash'] = hash
                            batch.append(dados)
                            count -= 1
                            if count == 0:
                                self.mongodb_manager.inserir_dados(batch)
                                count = 10000
                                
                                timestamp = datetime.now().strftime("%H:%M:%S")
                                sucesso(f'[{timestamp}] Inserindo {len(batch)} credenciais')
                                batch = []
                        except Exception as e:
                            erro(f'Erro ao processar linha {linha}: {str(e)}')

        except Exception as e:
            erro(f'Erro ao processar arquivo {arquivo.nome}: {str(e)}')

class MenuInterativo:
    def __init__(self):
        self.processador = ProcessadorArquivos()

    def exibir(self) -> None:
        while True:
            if not self._mostrar_opcoes():
                break
            
            opcao = self._obter_escolha()
            if opcao is None:
                break
            self.processador.processar_arquivo(opcao)

    def _mostrar_opcoes(self) -> bool:
        arquivos = self.processador.listar_arquivos_txt()
        
        sucesso('\n=== Menu de Arquivos TXT ===')
        
        if not arquivos:
            erro('Nenhum arquivo .txt encontrado na pasta!')
            return False
        
        for i, arquivo in enumerate(arquivos, 1):
            info(f'{i}. {arquivo.nome}')
        info('0. Sair')
        
        return True

    def _obter_escolha(self) -> Optional[ArquivoTXT]:
        arquivos = self.processador.listar_arquivos_txt()
        try:
            escolha = int(input('\nEscolha um arquivo (0 para sair): '))
            
            if escolha == 0:
                return None
            if 1 <= escolha <= len(arquivos):
                return arquivos[escolha - 1]
            
            erro('\nOpção inválida!')
        except ValueError:
            erro('\nPor favor, digite um número válido!')
        return None

def main():
    try:
        menu = MenuInterativo()
        menu.exibir()
    except KeyboardInterrupt:
        erro('\nPrograma encerrado pelo usuário')
    except Exception as e:
        erro(f'Erro inesperado: {str(e)}')

if __name__ == '__main__':
    main()

