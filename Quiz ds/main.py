import openai

chave_api = "insira a chave aqui"
openai.api_key = chave_api

def enviar_mensagem(mensagem, lista_mensagens=[]):
    lista_mensagens.append(
        {"role": "user", "content": mensagem}
    )
    
    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=lista_mensagens
    )

    return resposta["choices"][0]["message"]

lista_mensagens = [
    {"role": "system", "content": "Você é um professor. O aluno irá definir um tema, e você deverá criar uma pergunta com cinco alternativas, sendo uma correta, o aluno vai escolher uma dentre as 5 alternativas, se ele escolher a incorreta você dira q esta errada e passara para proxima, se ele estiver certo você vai dizer que esta certa e vai passar para proxima e não pode se repetir, nem as questões nem as alternativas. o aluno da o tema, e você faz questões com o tema, você da a questão o aluno responde e você da a proxima, sempre no final de cada questão deixe um marcador que inicia no 0/5, a cada questão esse marcador aumenta em 1, se o aluno errar ele não se altera, o aluno vence se o marcador estiver no 3/5 ou acima por isso sempre lembre de aumentar o marcador ou de não alterar ele, para você saber quanto está, você encerrará a sessão indicando o resultado final."}
]

contador = 0

while True:
    if contador == 0:
        texto = "Escreva o tema do quiz:"
    else:
        texto = "(ou escolha uma alternativa):"
    
    resposta = enviar_mensagem(texto, lista_mensagens)
    lista_mensagens.append(resposta)["content"]
    print("Quiz: ", resposta)
    
    contador += 1
    
    if contador >= 6:
        print("Quiz: O quiz foi finalizado.")
        break