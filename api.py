# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request
app = Flask(__name__)


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
    user_id = req['session']['user_id']

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.

        res['response']['text'] = 'Привет! Это игра Подземелья и драконы, чтобы узнать правила, скажите раскажи правила. ' \
                                  'Назовите имя и выберетие одного из четырёх персонажей для начала путишествия.' \
                                  'Персонажи: Эльф, маг, варвар, рыцарь. Для просмотра способномтей скажите скажи список способностей'
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
                                        'каждый ход ты сталкиваешься с событиями, они могут как прибавлять здоровье, так и отнимать' \
                                        'при каждом событии надо бросать кубик щита, он определяет, будешь ли ты наносить урон или получать хил' \
                                        'кубик щита в деапозоне от одного до двадцати' \
                                        'если вы пробили щит врага, то вы бросаете кубик урона, кубик урона для каждого персонажа разный'
            return
    except Exception:
        pass

    # Обрабатываем ответ пользователя.
    if req['request']['original_utterance'].lower() in [
        'ладно',
        'куплю',
        'покупаю',
        'хорошо',
    ]:
        # Пользователь согласился, прощаемся.
        res['response']['text'] = 'Раба можно найти на Яндекс.Маркете!'
        return

    # Если нет, то убеждаем его купить слона!
    res['response']['text'] = 'Все говорят "%s", а ты купи раба!' % (
        req['request']['original_utterance']
    )

# Функция возвращает две подсказки для ответа.

if __name__ == '__main__':
    app.run()