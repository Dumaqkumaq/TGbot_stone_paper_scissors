import telebot as tb
from telebot import types
from random import randint

token = open("token.txt").readline()
bot = tb.TeleBot(token)
emoj = ['🗿', '📄', '✂️']
results = ['Ваша победа!\nНаполняйте бокалы!', 'Ничья.\nСмиритесь с этим.', 'Вы проиграли...\nУдача не на вашей стороне']

#
# ЗАПИСЬ\ИЗМЕНЕНИЕ СТАТЫ В ФАЙЛ(Е)
# ЕСЛИ НОВЫЙ АЙДИ, ТО ЗАПИСЫВАЕМ В ФАЙЛ
#
def write_res(id, res):
    lines = open('stats.txt','r').readlines()
    write_line = ''
    for idx, line in enumerate(lines):
        if str(id) in line:
            # 1 =wins 2=draw 3=lose
            #id0 allgames1 wins2 draws3 loses4
            splitted = line.split()
            if(res == 1):
                splitted[1] =  str(int(splitted[1]) + 1)
                splitted[2] = str(int(splitted[2]) + 1)
            elif(res == 2):
                splitted[1] =  str(int(splitted[1]) + 1)
                splitted[3] = str(int(splitted[3]) + 1)
            elif (res == 3):
                splitted[1] =  str(int(splitted[1]) + 1)
                splitted[4] = str(int(splitted[4]) + 1)
            elif (res == 4):
                rer = str(splitted[1])+' ' + str(splitted[2])+' '+ str(splitted[3])+ ' '+ str(splitted[4])
                return rer
            elif (res == 0):
                for i in range(1,5):
                    splitted[i] = '0'
            lines[idx] = ' '.join(splitted) + '\n'
            with open('stats.txt', 'w') as f:
                f.writelines(lines)
            break
    else:
        if (res == 1):
            write_line = f'{id} 1 1 0 0'
            with open('stats.txt', 'a') as f:
                f.write(write_line + '\n')
            return '1 1 0 0'
        elif (res == 2):
            write_line = f'{id} 1 0 1 0'
            with open('stats.txt', 'a') as f:
                f.write(write_line + '\n')
            return '1 0 1 0'
        elif (res == 3):
            write_line = f'{id} 1 0 0 1'
            with open('stats.txt', 'a') as f:
                f.write(write_line + '\n')
            return '1 0 0 1'
        elif (res == 4):
            write_line = f'{id} 0 0 0 0'
            with open('stats.txt', 'a') as f:
                f.write(write_line+'\n')
            return '0 0 0 0'


#ПРИВЕТСТВИЕ
@bot.message_handler(commands=['start'])
def start(msg):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Играть")
    btn2 = types.KeyboardButton('Статистика')
    markup.add(btn1, btn2)
    bot.send_message(msg.from_user.id, "Приветствую!\nЭтот бот позволяет сыграть в камень,ножницу,бумагу!\nДля старта нажми на \"Cтарт\"\nДля просмотра статы нажми на \"Статистика\"", reply_markup=markup)

#РЕАКЦИИ НА СООБЩЕНИЯ
@bot.message_handler(content_types=['text'])
def get_text_msg(msg):
    if msg.text == 'Играть':
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text = 'Камень🗿', callback_data='stone')
        btn2 = types.InlineKeyboardButton(text='Бумага📄', callback_data='paper')
        btn3 = types.InlineKeyboardButton(text='Ножницы✂️', callback_data='scissors')
        markup.add(btn1, btn2, btn3)
        bot.send_message(msg.from_user.id, "Что сыграете?", reply_markup=markup)
    elif msg.text == 'Статистика':
        stat = write_res(msg.from_user.id, 4).split()
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text='Играть', callback_data='play')
        btn2 = types.InlineKeyboardButton(text='Обнулить стату', callback_data='clear_stats')
        bot.send_message(msg.from_user.id, f"Ваша статистика:\n  Всего игр:{stat[0]}\n  Победы:{stat[1]}\n  Ничья:{stat[2]}\n  Проигрыши:{stat[3]}")
        markup.add(btn1,btn2)
        bot.send_message(msg.from_user.id, "Сыграем?", reply_markup=markup)

# 1 = stone, 2 =paper, 3 = scissors
# 1 = win 2 = draw 3 = lose

#РЕАКЦИИ НА КНОПКИ
@bot.callback_query_handler(func = lambda call: True)
def callback_handler(call):
    #юзер выбрал игру
    if(call.data == 'stone' or call.data == 'paper' or call.data =='scissors'):
        bot_txt = 'Бот выбрал: '
        user_txt = 'Вы выбрали: '
        final_txt = 'Результат дуэли: '
        bot_ans = randint(0, 2)
        if call.data == 'stone':
            user_txt+= emoj[0]
            if(bot_ans == 0):
                bot_txt+= emoj[0]
                final_txt += results[1]
                write_res(call.message.chat.id, 2)
            elif(bot_ans == 1):
                bot_txt += emoj[1]
                final_txt += results[2]
                write_res(call.message.chat.id, 3)
            elif (bot_ans == 2):
                bot_txt += emoj[2]
                final_txt += results[0]
                write_res(call.message.chat.id, 1)
        elif call.data == 'paper':
            user_txt+= emoj[1]
            if(bot_ans == 0):
                bot_txt+= emoj[0]
                final_txt += results[0]
                write_res(call.message.chat.id, 1)
            elif(bot_ans == 1):
                bot_txt += emoj[1]
                final_txt += results[1]
                write_res(call.message.chat.id, 2)
            elif (bot_ans == 2):
                bot_txt += emoj[2]
                final_txt += results[2]
                write_res(call.message.chat.id, 3)
        elif call.data == 'scissors':
            user_txt+= emoj[2]
            if(bot_ans == 0):
                bot_txt+= emoj[0]
                final_txt += results[2]
                write_res(call.message.chat.id, 3)
            elif(bot_ans == 1):
                bot_txt += emoj[1]
                final_txt += results[0]
                write_res(call.message.chat.id, 1)
            elif (bot_ans == 2):
                bot_txt += emoj[2]
                final_txt += results[1]
                write_res(call.message.chat.id, 2)
        answer = bot_txt + '\n' + user_txt + '\n' + final_txt + '\n'

        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text ="Играть", callback_data= 'play')
        btn2 = types.InlineKeyboardButton(text ='Статистика', callback_data= 'stats')
        markup.add(btn1, btn2)
        bot.edit_message_text(answer, call.message.chat.id, call.message.message_id)
        bot.send_message(chat_id=call.message.chat.id, text="Сыграем вновь?", reply_markup=markup)
    #юзер выбрал игру с помощью инлайн кнопки
    elif(call.data == 'play'):
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text='Камень🗿', callback_data='stone')
        btn2 = types.InlineKeyboardButton(text='Бумага📄', callback_data='paper')
        btn3 = types.InlineKeyboardButton(text='Ножницы✂️', callback_data='scissors')
        markup.add(btn1, btn2, btn3)
        bot.edit_message_text(text="Что сыграете?", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
    #юзер выбрал показ статы
    elif(call.data == 'stats'):
        stat = write_res(call.message.chat.id, 4).split()
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text='Играть', callback_data='play')
        btn2 = types.InlineKeyboardButton(text='Обнулить стату', callback_data='clear_stats')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                         text=f"Ваша статистика:\n  Всего игр:{stat[0]}\n  Победы:{stat[1]}\n  Ничья:{stat[2]}\n  Проигрыши:{stat[3]}")
        markup.add(btn1, btn2)
        bot.send_message(call.message.chat.id, "Сыграем?", reply_markup=markup)
    #юзер выбрал обнуление статы
    elif(call.data == 'clear_stats'):
        write_res(call.message.chat.id, 0)
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text='Играть', callback_data='play')
        btn2 = types.InlineKeyboardButton(text='Обнулить стату', callback_data='clear_stats')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f"Ваша статистика обнулена")
        stat = write_res(call.message.chat.id, 4).split()
        bot.send_message(call.message.chat.id, f"Ваша статистика:\n  Всего игр:{stat[0]}\n  Победы:{stat[1]}\n  Ничья:{stat[2]}\n  Проигрыши:{stat[3]}", reply_markup=markup)
        markup.add(btn1, btn2)
        bot.send_message(call.message.chat.id, "Сыграем?", reply_markup=markup)


if __name__ == '__main__':
    print('-------------бот начал работу--------------')
    bot.infinity_polling()