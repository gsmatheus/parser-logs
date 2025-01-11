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
