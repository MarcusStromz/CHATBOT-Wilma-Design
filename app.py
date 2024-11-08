
import telebot
import dotenv
from os import getenv

dotenv.load_dotenv()

TOKEN_TELEGRAM = getenv('7327311762:AAF70LYsrczt5oL7186NMry63LrkkP3N-CY')

bot = telebot.TeleBot("7327311762:AAF70LYsrczt5oL7186NMry63LrkkP3N-CY")

user_choices = {}

comandos = (
    '/catalogo - Ver catálogo\n'
    '/agendar - Agendar serviço\n'
    '/suporte - Suporte\n'
)

@bot.message_handler(commands=['start'])
def mensagem_boas_vindas(message):
    nome_usuario = message.from_user.first_name
    mensagem = f'Olá, {nome_usuario}, meu nome é Wilma Santana e sou design de sobrancelhas e micropigmentação. Sou especialista em sobrancelhas sutilmente marcantes e utilizo o método exclusivo Unic Brows. Em que posso ajudar?\n\nEscolha uma das opções abaixo:\n{comandos}'
    bot.send_message(message.chat.id, mensagem)

@bot.message_handler(commands=['catalogo'])
def ver_catalogo(message):
    with open('C:/Users/marcu/Downloads/Catálogo Sobrancelha s.pdf', 'rb') as catalogo:
        bot.send_document(message.chat.id, catalogo)
    bot.send_message(
        message.chat.id,
        "Escolha uma das opções abaixo:\n/opcao_servico - Escolher Serviço\n/menu_principal - Voltar ao menu principal"
    )

@bot.message_handler(commands=['opcao_servico'])
def opcao_servico(message):
    agendar_servico(message)  # Chama a função que inicia o agendamento

@bot.message_handler(commands=['agendar'])
def agendar_servico(message):
    user_choices[message.chat.id] = "aguardando_servico"
    opcoes = (
        "Escolha uma das opções abaixo para agendar:\n"
        "1. Sobrancelha\n"
        "2. Facial\n"
        "3. Outros Procedimentos\n"
    )
    bot.send_message(message.chat.id, opcoes)

@bot.message_handler(func=lambda message: message.chat.id in user_choices and user_choices[message.chat.id] == "aguardando_servico" and message.text in ['1', '2', '3'])
def escolher_servico(message):
    if message.text == '1':
        servicos = (
            "Escolha um serviço de Sobrancelha:\n"
            "1. Design Personalizado\n"
            "2. Design e Henna\n"
            "3. Design Reconstrutivo\n"
            "4. Design Recons + Henna\n"
            "5. Micropigmentação\n"
        )
    elif message.text == '2':
        servicos = (
            "Escolha um serviço Facial:\n"
            "1. Detox Facial\n"
            "2. Dermaplaning\n"
        )
    else:  # message.text == '3'
        servicos = (
            "Escolha um serviço de Outros Procedimentos:\n"
            "1. Lash Lifting\n"
            "2. Depilação de Buço\n"
            "3. Buço + Queixo\n"
            "4. Depilação Axila\n"
        )
    
    user_choices[message.chat.id] = "aguardando_servico_escolhido"
    bot.send_message(message.chat.id, servicos)

@bot.message_handler(func=lambda message: message.chat.id in user_choices and user_choices[message.chat.id] == "aguardando_servico_escolhido" and message.text in ['1', '2', '3', '4', '5'])
def servico_escolhido(message):
    if message.text in ['1', '2', '3', '4', '5']:
        # Armazenar a escolha do serviço
        if user_choices[message.chat.id] == "aguardando_servico_escolhido":
            user_choices[message.chat.id] = "servico_selecionado"
        
        # Enviar opções para marcar horário ou escolher outro serviço
        opcoes_finais = (
            "Escolha:\n"
            "1. Marcar horário\n"
            "2. Escolher outro serviço\n"
        )
        bot.send_message(message.chat.id, opcoes_finais)

@bot.message_handler(func=lambda message: message.chat.id in user_choices and user_choices[message.chat.id] == "servico_selecionado" and message.text in ['1', '2'])
def opcoes_final(message):
    if message.text == '1':
        bot.send_message(message.chat.id, "Ótimo! Vamos marcar o seu horário. Funcionamos de segunda a sexta de 14:00 até 20:00 e Sábado de 8:00 até 17:00. Por favor, envie o horário desejado.")
        user_choices[message.chat.id] = "aguardando_horario"
    elif message.text == '2':
        bot.send_message(message.chat.id, "Por favor, escolha um serviço:\n"
                                            "/agendar - Agendar novo serviço\n"
                                            "/menu_principal - Voltar ao menu principal")

@bot.message_handler(func=lambda message: message.chat.id in user_choices and user_choices[message.chat.id] == "aguardando_horario")
def receber_horario(message):
    # Armazenar o horário desejado
    user_choices[message.chat.id] = "horario_selecionado"
    bot.send_message(message.chat.id, "Perfeito, logo entraremos em contato confirmando seu agendamento. Gostaria de avaliar o atendimento com um feedback?")
    
    # Oferecer opções de feedback
    feedback_opcoes = (
        "1. Sim\n"
        "2. Não\n"
    )
    bot.send_message(message.chat.id, feedback_opcoes)

@bot.message_handler(func=lambda message: message.chat.id in user_choices and user_choices[message.chat.id] == "horario_selecionado" and message.text in ['1', '2'])
def feedback_usuario(message):
    if message.text == '1':
        bot.send_message(message.chat.id, "Por favor, deixe seu feedback.")
        user_choices[message.chat.id] = "aguardando_feedback"
    elif message.text == '2':
        bot.send_message(message.chat.id, "Agradecemos pelo seu atendimento! Voltando ao menu principal.")
        user_choices[message.chat.id] = None  # Reseta a escolha do usuário

@bot.message_handler(func=lambda message: message.chat.id in user_choices and user_choices[message.chat.id] == "aguardando_feedback")
def receber_feedback(message):
    feedback = message.text
    bot.send_message(message.chat.id, f"Agradecemos pelo seu feedback: '{feedback}'! Voltando ao menu principal.")
    user_choices[message.chat.id] = None  # Reseta a escolha do usuário

@bot.message_handler(commands=['suporte'])
def suporte(message):
    bot.send_message(message.chat.id, 'Você escolheu Suporte. Como posso ajudar?')

@bot.message_handler(func=lambda message: 'Bom dia' in message.text)
def responde_usuario(message): 
    nome_usuario = message.from_user.first_name
    resposta = f'Olá, {nome_usuario}. Em que posso ajudar?'
    bot.reply_to(message, resposta)

if __name__ == '__main__':
    bot.polling()