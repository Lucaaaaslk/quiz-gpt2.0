import openai
from flask import Flask, render_template, request

app = Flask(__name__)

chave_api = "insira a chave aqui"
openai.api_key = chave_api

lista_mensagens = [
      {"role": "system", "content": "Você é um professor. O aluno irá definir um tema, e você deverá criar uma pergunta com cinco alternativas, sendo uma correta, o aluno vai escolher uma dentre as 5 alternativas, se ele escolher a incorreta você dira q esta errada e passara para proxima, se ele estiver certo você vai dizer que esta certa e vai passar para proxima e não pode se repetir, nem as questões nem as alternativas. o aluno da o tema, e você faz questões com o tema, você da a questão o aluno responde e você da a proxima, sempre no final de cada questão deixe um marcador que inicia no 0/5 ao mesmo tmepo ja cite as proximas 5 alternativas, a cada questão esse marcador aumenta em 1, se o aluno errar ele não se altera, o aluno vence se o marcador estiver no 3/5 ou acima por isso sempre lembre de aumentar o marcador ou de não alterar ele, para você saber quanto está, você encerrará a sessão indicando o resultado final."}
]

contador = 0

def enviar_mensagem(mensagem, lista_mensagens):
    lista_mensagens.append({"role": "user", "content": mensagem})
    
    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  
        messages=lista_mensagens
    )
    
    return resposta.choices[0].message

@app.route('/', methods=['GET', 'POST'])
def chatbot():
    global contador

    if contador == 0:
        initial_message = "Escreva o tema do quiz:"
        lista_mensagens.append({"role": "assistant", "content": initial_message})

    if request.method == 'POST':
        user_input = request.form['user_input']
        response = enviar_mensagem(user_input, lista_mensagens)
        lista_mensagens.append(response)
        
        contador += 1

        if contador >= 6:
            final_message = "Quiz: O quiz foi finalizado."
            return render_template('index.html', response_gpt=lista_mensagens, final_message=final_message)

        next_prompt = "Escreva sua resposta (ou escolha uma alternativa, espere 20 segundos para cada interação):"
        lista_mensagens.append({"role": "assistant", "content": next_prompt})

        return render_template('index.html', response_gpt=lista_mensagens)

    return render_template('index.html', response_gpt=lista_mensagens)

if __name__ == '__main__':
    app.run(debug=True)
