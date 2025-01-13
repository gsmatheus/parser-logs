import time

from pymongo import MongoClient
from typing import List, Dict, Any
from datetime import datetime
from utils import info, erro, sucesso


class MongoDBManager:
    def __init__(self, connection_string: str = "mongodb://mongo:e667596cf465203b976f@198.7.115.135:27018/?tls=false"):
        self.client = MongoClient(connection_string)
        self.db = self.client.logs
        self.collection = self.db.logs1
        
        # Verifica se conexão foi estabelecida
        try:
            self.client.admin.command('ping')
            info("Conexão com o MongoDB estabelecida com sucesso")
        except Exception as e:
            erro(f"Erro ao estabelecer conexão com o MongoDB: {e}")

    def inserir_dados(self, dados: List[Dict[str, Any]]) -> None:
        documentos = []
        try:
            start_time = time.time()
            for dado in dados:
                documento = {
                    "url": dado['url'],
                    "login": dado['email'],
                    "senha": dado['senha'],
                    "hash": dado['hash']
                }
                documentos.append(documento)
        
            if documentos:
                self.collection.insert_many(documentos, ordered=False)
            end_time = time.time()
            elapsed_time = end_time - start_time
            info(f"Tempo de inserção: {elapsed_time:.2f} segundos")
        except Exception as e:
            if "E11000 duplicate key error" in str(e):
                return
            else:
                with open("log_error.txt", "a") as arquivo:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    arquivo.write(f"[{timestamp}] Erro: {str(e)}\n")

    def criar_collection_credenciais(self, nome_collection: str = "logs1") -> None:
        self.collection = self.db[nome_collection]
        self.collection.create_index("hash", unique=True)

    def fechar_conexao(self) -> None:
        self.client.close() 