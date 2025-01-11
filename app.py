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

url_entrada = "https://sistema.sismix.com.br:8080/cadastro:luizfelipesoaresdm@outlook.com:Zfa#5+livre"
resultado = extrair_dados(url_entrada)

print(resultado['senha'])
print(resultado['email'])
print(resultado['url'])
print(contar_pontos(url_entrada))