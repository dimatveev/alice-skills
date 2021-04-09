from __future__ import unicode_literals
from data import db_session

import json
import logging
#from flask_ngrok import run_with_ngrok

from flask import Flask, request


app = Flask(__name__)
#app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

#run_with_ngrok(app)

etap = 'askname'
state = {}
fights = 0
#elf = Elf()

logging.basicConfig(level=logging.DEBUG)

@app.route("/", methods=['POST'])

def main():
# Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )
# Функция для непосредственной обработки диалога.
def handle_dialog(req, res):
    global etap
    global state
    global fights
    #global elf
    user_id = req['session']['user_id']

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.
        res['response']['text'] = 'Привет! Это игра Подземелья и драконы, чтобы узнать правила, скажите раскажи правила. ' \
                                  'Назовите имя и после подтверждения выберетие одного из четырёх персонажей для начала путишествия. ' \
                                  'Персонажи: Эльф, маг, варвар, рыцарь. Для просмотра способномтей отдельного персонажа' \
                                  ' скажите "какие способности у ..." '
        return

    try:  # на всякий случай)
        if list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['закончить', 'диалог'] or \
                list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['останови', 'диалог'] or \
                    list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['завершить', 'диалог']:
            res['response'][
                'text'] = 'Пока! Захочешь повторить магическое путешествие, я всегда тут!'
            res['response'][
                'tts'] = 'Пока! Захочешь повторить магическое путешествие, я всегда тут!'
            res['response']['end_session'] = True
            return
    except Exception:
        pass
    try:
        # что ты умеешь? - обязательный вопрос в навыке Алисы
        if list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['какие', 'способности', 'эльфа'] or \
                list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['способности', 'у', 'эльфа'] or \
                    list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['какие', 'способности', 'у' 'эльфа'] or \
                        list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['способности', 'эльфа']:
            res['response']['text'] = 'начальное здоровье эльфа - 12, максимальный урон эльфа - 6, щит эльфа - 17 ' \
                                      'приёмы эльфа:Первый - стрельба из лука, второй - захват лозой, третий - удар кинжалом '
            return
    except Exception:
        pass

    try:
        # что ты умеешь? - обязательный вопрос в навыке Алисы
        if list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['какие', 'способности', 'рыцаря'] or \
                list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['способности', 'у', 'рыцаря'] or \
                    list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['какие', 'способности', 'у' 'рыцаря'] or \
                        list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['способности', 'рыцаря']:
            res['response']['text'] = 'начальное здоровье рыцаря - 13, максимальный урон рыцаря - 5, щит рыцаря - 17 ' \
                                      'приёмы рыцаря:Первый - удар мечём , второй - толчок щитом, третий - укол копьём '
            return
    except Exception:
        pass

    try:
        # что ты умеешь? - обязательный вопрос в навыке Алисы
        if list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['какие', 'способности', 'мага'] or \
                list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['способности', 'у', 'мага'] or \
                    list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['какие', 'способности', 'у' 'мага'] or \
                        list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['способности', 'мага']:
            res['response']['text'] = 'начальное здоровье мага - 11, максимальный урон мага - 6, щит мага - 18 ' \
                                      'приёмы мага:Первый - фаербол, второй - энэргосфера, третий - теликинез '
            return
    except Exception:
        pass

    try:
        # что ты умеешь? - обязательный вопрос в навыке Алисы
        if list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['какие', 'способности', 'варвара'] or \
                list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['способности', 'у', 'варвара'] or \
                    list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['какие', 'способности', 'у' 'варвара'] or \
                        list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['способности', 'варвара']:
            res['response']['text'] = 'начальное здоровье варвара - 14, максимальный урон варвара - 7, щит варвара - 16 ' \
                                      'приёмы варвара:Первый - удар секирой, второй - бросок топора, третий - удар моргенштерном '
            return
    except Exception:
        pass

    try:
        # что ты умеешь? - обязательный вопрос в навыке Алисы
        if list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['что', 'ты', 'умеешь'] or \
                list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['помощь']:
            res['response']['text'] = 'Я умею запускать игру Подземелья и Драконы, где пользователь сталкивается с разными препятствиями ' + \
                                        'в эту игру можно играть даже одному, потому что ведущий - это Алиса'
            return
    except Exception:
        pass

    try:
        # что ты умеешь? - обязательный вопрос в навыке Алисы
        if list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['профиль'] or \
                list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['пользователь']:
            res['response']['text'] = f'Имя:{state["name"]}\n' \
                                      f'Герой:{state["role"]}\n' \
                                      f'Хп:{state["hp"]}\n' \
                                      f'Щит:{state["shield"]}\n' \
                                      f'Минимальная атака:{state["mina"]}\n' \
                                      f'Максимальная атака:{state["maxa"]}'
            return
    except Exception:
        pass

    try:
        # правила
        if list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['расскажи', 'правила'] or \
                list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['какие', 'правила'] or \
                    list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['правила']:
            res['response']['text'] = 'В этой игре ты выбираешь одного из четырёх персонажей, эльф, маг, варвар, рыцарь ' + \
                                        'каждый ход ты сталкиваешься с событиями, они могут как прибавлять здоровье, так и отнимать ' \
                                        'при каждом событии надо бросать кубик щита, он определяет, будешь ли ты наносить урон или получать хил ' \
                                        'кубик щита в деапозоне от одного до двадцати ' \
                                        'если вы пробили щит врага, то вы бросаете кубик урона, кубик урона для каждого персонажа разный'
            return
    except Exception:
        pass

    try:  # на всякий случай)
        if state["hp"] <=0:
            res['response'][
                'text'] = 'Пока! Захочешь повторить магическое путешествие, я всегда тут!'
            res['response'][
                'tts'] = 'Пока! Захочешь повторить магическое путешествие, я всегда тут!'
            res['response']['end_session'] = True
            return
    except Exception:
        pass

    if etap == 'ending':
        if req["request"]["original_utterance"].lower() in ["награда", "получить награду"]:
            res["response"]["text"] = f"Спасибо тебе храбрый {state['role']} {state['name']},  в награду ты получашь " \
                                      f"признание людей! Если захочешь поиграть ещё, я всегда тут "
            res['response']['end_session'] = True
        else:
            res["response"]["text"] = f"Спасибо тебе храбрый {state['role']} {state['name']},  в награду ты получашь " \
                                      f"признание людей! Если захочешь поиграть ещё, я всегда тут "
            res['response']['end_session'] = True

    elif etap == 'fight':
        if fights == 0:
            if req["request"]["original_utterance"].lower() in ["начать приключение", "начни приключение"]:
               res["response"]["text"] = f"Вы наткнулись на врага"
               # res["response"]["text"] = f"Вы наткнулись на {elf.enemy}"
            else:
                res["response"]["text"] = "Напоминаю, чтобы начать скажите 'начать приключение'"

    elif etap == 'begin':
        if req["request"]["original_utterance"].lower() in ["продолжить", "дальше"]:
            res["response"]["text"] = "Хорошо! Чтобы отправиться в путь скажите 'начать приключение', не забывайте говорить " \
                                      "'брось кубики',состояние игрока можно проверить командой профиль \n" \
                                      "Также вы можете узнать профиль игрока, сказав 'профиль' "
            etap = 'fight'
        else:
            res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить'"
    #Профиль: res["response"]["text"] =
    #хп
    #роль
    #кол-во пройденых этапов
    #

    elif etap == 'askrole':
        role = req["request"]["original_utterance"]
        state["role"] = role
        if role == "эльф":
            res["response"]["text"] = "Отлично! вы меткий эльф из лесов. \n Чтобы пройти дальше, скажите 'продолжить'"
            etap = 'begin'
            state["hp"] = 12
            state["shield"] = 17
            state["mina"] = 2
            state["maxa"] = 6
        elif role == "рыцарь":
            res["response"]["text"] = "Отлично! вы бесстрашный воин королевства. \n Чтобы пройти дальше, скажите 'продолжить'"
            etap = 'begin'
            state["hp"] = 13
            state["shield"] = 17
            state["mina"] = 2
            state["maxa"] = 5
        elif role == "маг":
            res["response"]["text"] = "Отлично! вы мудрый чародей башни. \n Чтобы пройти дальше, скажите 'продолжить'"
            etap = 'begin'
            state["hp"] = 11
            state["shield"] = 18
            state["mina"] = 2
            state["maxa"] = 6
        elif role == "варвар":
            res["response"]["text"] = "Отлично! вы грозный варвар из гор. \n Чтобы пройти дальше, скажите 'продолжить'"
            etap = 'begin'
            state["hp"] = 14
            state["shield"] = 16
            state["mina"] = 2
            state["maxa"] = 7
        else:
            res["response"]["text"] = "Повторите роль ещё раз, напоминаю, у вас всего четыре варианта: эльф, маг, рыцарь или варвар"

    elif etap == 'checkname':
        if req["request"]["original_utterance"].lower() in ["да", "правильно"]:
            res["response"]["text"] = f'Приятно познокомиться, {state["name"]}. Теперь назовите персонажа, Для просмотра способномтей определённого персонажа' \
                          ' скажите "какие способности у ..."'
            etap = 'askrole'
        elif req["request"]["original_utterance"].lower() in ["нет", "не правильно", "заново"]:
            res["response"]["text"] = "Повторите имя, пожалуйста"
            etap = 'askname'

    elif etap == 'askname':
        state["name"] = req["request"]["original_utterance"]
        res["response"]["text"] = f'Супер! Правильно ли я поняла, что вас зовут {state["name"]}?'
        etap = 'checkname'


if __name__ == '__main__':
        db_session.global_init("db/event.db")
        app.run()