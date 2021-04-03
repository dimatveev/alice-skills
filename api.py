# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request
app = Flask(__name__)

etap = 1

logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.

# Задаем параметры приложения Flask.
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

    if etap == 3:
        if req["request"]["original_utterance"].lower() in ["продолжить", "дальше"]:
            res["response"]["text"] = "Хорошо! сейчас начнётся приключение, не забывайте говорить 'брось кубики',состояние игрока можно проверить командой профиль "
        else:
            res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить'"
    #Профиль: имя
    #хп
    #роль
    #кол-во пройденых этапов
    #

    if etap == 2:
        role = req["request"]["original_utterance"]
        if role == "эльф":
            res["response"]["text"] = "Отлично! вы меткий эльф из лесов. \n Чтобы пройти дальше, скажите 'продолжить'"
            etap += 1
            #Таблица = таблица эльфа
        elif role == "рыцарь":
            res["response"]["text"] = "Отлично! вы бесстрашный воин королевства. \n Чтобы пройти дальше, скажите 'продолжить'"
            etap += 1
            #Таблица = таблица рыцаря
        elif role == "маг":
            res["response"]["text"] = "Отлично! вы мудрый чародей башни. \n Чтобы пройти дальше, скажите 'продолжить'"
            etap += 1
            #Таблица = таблица мага
        elif role == "варвар":
            res["response"]["text"] = "Отлично! вы грозный варвар из гор. \n Чтобы пройти дальше, скажите 'продолжить'"
            etap += 1
            #Таблица = таблица варвара
        else:
            res["response"]["text"] = "Повторите роль ещё раз, напоминаю, у вас всего четыре варианта: эльф, маг, рыцарь или варвар"

    if etap == 1:
        name = req["request"]["original_utterance"]
        res["response"]["text"] = f"Супер! Правильно ли я поняла, что вас зовут {name}?"
        if req["request"]["original_utterance"].lower() in ["да", "правильно"]:
            res["response"]["text"] = f'Приятно познокомиться, {name}. Теперь назовите персонажа, Для просмотра способномтей определённого персонажа' \
                          ' скажите "какие способности у ..."'
            etap += 1
        elif req["request"]["original_utterance"].lower() in ["нет", "не правильно", "заново"]:
            res["response"]["text"] = "Повторите имя, пожалуйста"


    # Обрабатываем ответ пользователя.
#    if req['request']['original_utterance'].lower() in [
#        'ладно',
#        'куплю',
#        'покупаю',
#        'хорошо',
#    ]:
#        # Пользователь согласился, прощаемся.
#        res['response']['text'] = 'Раба можно найти на Яндекс.Маркете!'
#        return

    # Если нет, то убеждаем его купить слона!
#    res['response']['text'] = 'Все говорят "%s", а ты купи раба!' % (
#        req['request']['original_utterance']
#    )

# Функция возвращает две подсказки для ответа.

if __name__ == '__main__':
    app.run()