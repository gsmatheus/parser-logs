import hashlib

GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def contar_pontos(url_completa):
    return url_completa.count(':')

def extrair_dados(url_completa):
    dados_invertidos = url_completa[::-1]
    partes = dados_invertidos.split(':', 3)

    senha = partes[0]
    email = partes[1]
    url = partes[2:]

    return {
        'senha': senha[::-1],
        'email': email[::-1],
        'url': ':'.join(url)[::-1]
    }

def sucesso(mensagem):
    print(f"{GREEN}{BOLD}{mensagem}{RESET}")

def info(mensagem):
    print(f"{BLUE}{BOLD}{mensagem}{RESET}")

def erro(mensagem):
    print(f"{RED}{BOLD}{mensagem}{RESET}")

hashes = []
todos = []
docs = []

def gera_hash(line):
    return hashlib.md5(line.encode()).hexdigest()

def verifica_hash(hash):
    return hash in hashes

def separa_informacoes(line):
    partes = line.strip().split(":")
    if len(partes) >= 3:
        return partes[0], partes[1], partes[2]
    return None, None, None

def processar_linhas(file_path, arquivo_unicas):
    i = 0

    try:
        with open(arquivo_unicas, 'w', encoding='utf-8') as arq_unicas, \
             open(file_path, 'r', encoding='utf-8') as f:

            for line in f:
                i += 1

                hash_line = gera_hash(line)

                if verifica_hash(hash_line):
                    print(f"Linha {i} duplicada: {line.strip()}")
                    continue

                hashes.append(hash_line)

                part1, part2, part3 = separa_informacoes(line)
                if part1 and part2 and part3:
                    arq_unicas.write(line)

    except FileNotFoundError:
        print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")
