from __future__ import unicode_literals
from data import db_session
from data.wizards import Wizard
from data.elfs import Elf
from data.barbarians import Barbarian
from data.knights import Knight
import json
import random
import logging


from flask import Flask, request

app = Flask(__name__)
db_session.global_init("db/event.db")
db_sess = db_session.create_session()


class State:
    def __init__(
            self,
            etap='askname',
            state=None,
            stateen=None,
            fights=0,
            fight_step=1,
            shi=0,
            atc=0,
            num=None,
    ):
        self.etap = etap
        self.state = state or {}
        self.stateen = stateen or {}
        self.fights = fights
        self.num = num
        self.fight_step = fight_step
        self.shi = shi
        self.atc = atc
        self.num = [1, 3, 4, 6, 7, 8, 9, 10, 11, 13]

    def to_dict(self):
        return self.__dict__



logging.basicConfig(level=logging.DEBUG)


@app.route("/", methods=['POST'])
def main(): 
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


def handle_dialog(req, res):
    user_id = req['session']['user_id']

    state_dict = req.get('state', {}).get('user') or {}
    state: State = State(**state_dict)

    if req['session']['new']:
        res['response']['text'] = 'Привет! Это игра Подземелья и драконы, в этой игре вы можете отправиться в захватывающее приключение' \
                                  ', играя за одного из четырех персонажей. Чтобы узнать правила, скажите раскажи правила. ' \
                                  'Назовите имя и после подтверждения выберетие одного из четырёх персонажей для начала путишествия. ' \
                                  'Персонажи: Эльф, маг, варвар, рыцарь. Для просмотра способностей отдельного персонажа' \
                                  ' скажите "какие способности у мага" '
        res['response']['tts'] = '<speaker audio="alice-sounds-game-boot-1.opus"> Привет! Это игра Подземелья и драконы,' \
                                 ' в этой игре вы можете отправиться в захватывающее приключение, играя за одного из четырех персонажей.' \
                                 ' Чтобы узнать правила, скажите раскажи правила. ' \
                                  'Назовите имя и после подтверждения выберетие одного из четырёх персонажей для начала путишествия. ' \
                                  'Персонажи: Эльф, маг, варвар, рыцарь. Для просмотра способностей отдельного персонажа' \
                                  ' скажите "какие способности у мага" '
        res['user_state_update'] = state.to_dict()
        return

    try:
        if list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['закончить', 'диалог'] or \
                list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['останови', 'диалог'] or \
                list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['закончи', 'прикдючение'] or \
                list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['стоп'] or \
                list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['хватит']:
            res['response']['text'] = 'Пока! Захочешь повторить магическое путешествие, я всегда тут!'
            res['response']['tts'] = '<speaker audio="alice-sounds-game-boot-1.opus"> Пока! Захочешь повторить магическое путешествие, я всегда тут!'
            state.state = {}
            state.etap = "askname"
            state.fights = 0
            state.fight_step = 1
            state.num = [1, 3, 4, 6, 7, 8, 9, 10, 11, 13]
            res['response']['end_session'] = True
            res['user_state_update'] = state.to_dict()
            return
    except Exception:
        pass
    try:
        if list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['начать', 'заново'] or \
                list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['заново'] or \
                list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['снова']:
            res['response']['text'] = 'Хорошо, назовите имя ещё раз'
            res['response']['tts'] = '<speaker audio="alice-sounds-game-boot-1.opus"> Хорошо, назовите имя ещё раз'
            state.state = {}
            state.etap = "askname"
            state.fights = 0
            state.fight_step = 1
            state.num = [1, 3, 4, 6, 7, 8, 9, 10, 11, 13]
            res['user_state_update'] = state.to_dict()
            return
    except Exception:
        pass
    try:
        if list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['какие', 'способности', 'эльфа'] or \
                list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['способности', 'у', 'эльфа'] or \
                list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['какие', 'способности', 'у' 'эльфа'] or \
                list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['способности', 'эльфа']:
            res['response']['text'] = 'начальное здоровье эльфа - 12\n максимальный урон эльфа - 6\n щит эльфа - 17\n' \
                                      'приёмы эльфа: Первый - стрельба из лука\n второй - захват лозой\n третий - удар кинжалом '
            res['user_state_update'] = state.to_dict()
            return
    except Exception:
        pass

    try:
        if list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['какие', 'способности', 'рыцаря'] or \
                list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['способности', 'у', 'рыцаря'] or \
                list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['какие', 'способности', 'у' 'рыцаря'] or \
                list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['способности', 'рыцаря']:
            res['response']['text'] = 'начальное здоровье рыцаря - 13\n максимальный урон рыцаря - 5\n щит рыцаря - 17 \n' \
                                      'приёмы рыцаря: Первый - удар мечём \nвторой - толчок щитом \nтретий - укол копьём '
            res['user_state_update'] = state.to_dict()
            return
    except Exception:
        pass

    try:
        if list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['какие', 'способности', 'мага'] or \
                list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['способности', 'у', 'мага'] or \
                list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['какие', 'способности', 'у' 'мага'] or \
                list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['способности', 'мага']:
            res['response']['text'] = 'начальное здоровье мага - 11\n максимальный урон мага - 6\n щит мага - 18\n' \
                                      'приёмы мага: Первый - фаербол\n второй - энэргосфера\n третий - теликинез '
            res['user_state_update'] = state.to_dict()
            return
    except Exception:
        pass

    try:
        if list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['какие', 'способности', 'варвара'] or \
                list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['способности', 'у', 'варвара'] or \
                list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['какие', 'способности', 'у' 'варвара'] or \
                list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['способности', 'варвара']:
            res['response']['text'] = 'начальное здоровье варвара - 14\n максимальный урон варвара - 7\n щит варвара - 16\n' \
                                      'приёмы варвара: Первый - удар секирой\n второй - бросок топора\n третий - удар моргенштерном'
            res['user_state_update'] = state.to_dict()
            return
    except Exception:
        pass
    try:
        if list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['что', 'ты', 'умеешь'] or \
                list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['помощь']:
            res['response']['text'] = 'Я умею запускать игру Подземелья и Драконы, где пользователь сталкивается с разными препятствиями ' + \
                                      'в эту игру можно играть даже одному, потому что ведущий - это Алиса'
            res['response']['tts'] = '<speaker audio="alice-sounds-game-boot-1.opus"> Я умею запускать игру Подземелья ' \
                                     'и Драконы, где пользователь сталкивается с разными препятствиями ' + \
                                      'в эту игру можно играть даже одному, потому что ведущий - это Алиса'
            res['user_state_update'] = state.to_dict()
            return
    except Exception:
        pass

    try:
        if list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['профиль'] or \
                list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['пользователь']:
            res['response']['text'] = f'Имя:{state.state["name"]}\n' \
                                      f'Герой:{state.state["role"]}\n' \
                                      f'Хп:{state.state["hp"]}\n' \
                                      f'Щит:{state.state["shield"]}\n' \
                                      f'Минимальная атака:{state.state["mina"]}\n' \
                                      f'Максимальная атака:{state.state["maxa"]}'
            res['response']['tts'] = f'<speaker audio="alice-sounds-game-powerup-1.opus">'\
                                     f'Имя:{state.state["name"]}\n' \
                                     f'Герой:{state.state["role"]}\n' \
                                     f'Хп:{state.state["hp"]}\n' \
                                     f'Щит:{state.state["shield"]}\n' \
                                     f'Минимальная атака:{state.state["mina"]}\n' \
                                     f'Максимальная атака:{state.state["maxa"]}'
            res['user_state_update'] = state.to_dict()
            return
    except Exception:
        pass

    try:
        if list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['расскажи', 'правила'] or \
                list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['какие', 'правила'] or \
                list(map(lambda x: x.lower(), req['request']['nlu']['tokens'])) == ['правила']:
            res['response']['text'] = 'В этой игре ты выбираешь одного из четырёх персонажей, эльф, маг, варвар, рыцарь ' \
                                      'каждый ход ты сталкиваешься с врагами которые будут наносить тебе урон ' \
                                      'при каждом событии надо пробивать щит, он определяет, будешь ли ты наносить урон ' \
                                      'кубик щита в деапозоне от одного до двадцати ' \
                                      'если вы пробили щит врага, то вы бросаете кубик урона, кубик урона для каждого персонажа разный'
            res['response']['tts'] = '<speaker audio="alice-sounds-game-boot-1.opus"> В этой игре ты выбираешь одного из' \
                                     ' четырёх персонажей, эльф, маг, варвар, рыцарь ' \
                                      'каждый ход ты сталкиваешься с врагами которые будут наносить тебе урон ' \
                                      'при каждом событии надо пробивать щит, он определяет, будешь ли ты наносить урон ' \
                                      'кубик щита в деапозоне от одного до двадцати ' \
                                      'если вы пробили щит врага, то вы бросаете кубик урона, кубик урона для каждого персонажа разный'
            res['user_state_update'] = state.to_dict()
            return
    except Exception:
        pass

    if state.etap == 'ending':
        if req["request"]["original_utterance"].lower() in ["награда", "получить награду"]:
            res["response"]["text"] = f"Спасибо тебе храбрый {state.state['role']} {state.state['name']},  в награду ты получашь " \
                                      f"признание людей! Если захочешь поиграть ещё, я всегда тут "
            res["response"]["tts"] =  f'<speaker audio="alice-sounds-game-8-bit-coin-1.opus">'\
                                      f"Спасибо тебе храбрый {state.state['role']} {state.state['name']},  в награду ты получашь " \
                                      f"признание людей! Если захочешь поиграть ещё, я всегда тут "
            res['response']['end_session'] = True
            state.state = {}
            state.etap = "askname"
            state.fights = 0
            state.fight_step = 1
            state.num = [1, 3, 4, 6, 7, 8, 9, 10, 11, 13]
        else:
            res["response"]["text"] = f"Спасибо тебе храбрый {state.state['role']} {state.state['name']},  в награду ты получашь " \
                                      f"признание людей! Если захочешь поиграть ещё, я всегда тут "
            res["response"]["tts"] =  f'<speaker audio="alice-sounds-game-8-bit-coin-1.opus">'\
                                      f"Спасибо тебе храбрый {state.state['role']} {state.state['name']},  в награду ты получашь " \
                                      f"признание людей! Если захочешь поиграть ещё, я всегда тут "
            res['response']['end_session'] = True
            state.state = {}
            state.etap = "askname"
            state.fights = 0
            state.fight_step = 1
            state.num = [1, 3, 4, 6, 7, 8, 9, 10, 11, 13]

    elif state.etap == 'fight':
        if state.state["role"] == "маг":
            if state.fights == 3:
                n = 12
                wizard3 = db_sess.query(Wizard).filter(Wizard.id == n).first()
                if state.fight_step == 1:
                    state.stateen["enem_hp"] = wizard3.enemyhp
                    state.stateen["enem"] = wizard3.enemy
                    state.stateen["enemshi"] = wizard3.shield
                    state.stateen["enemmina"] = wizard3.minatack
                    state.stateen["enemmaxa"] = wizard3.maxatack
                    state.stateen["enemfirst"] = wizard3.firstkill
                    state.stateen["enemsecond"] = wizard3.secondkill
                    state.stateen["enemthird"] = wizard3.thirdkill
                    if req["request"]["original_utterance"].lower() in ["найти дракона", "искать дракона"]:
                        res["response"]["text"] = f"Вы встретили огромного дракона, сторожащего золото\n" \
                                                  f"Параметры дракона:\n" \
                                                  f"хп: {state.stateen['enem_hp']}\n" \
                                                  f"щит: {state.stateen['enemshi']}\n" \
                                                  f"минимальная атака: {state.stateen['enemmina']}\n" \
                                                  f"максимальная атака: {state.stateen['enemmaxa']}\n" \
                                                  f"Чтобы ударить дракона пробейте его щит, скажите 'пробить щит'"
                        state.fight_step = 2

                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить приключение'"
                elif state.fight_step == 2:
                    if req["request"]["original_utterance"].lower() in ["пробить щит", "пробей щит"]:
                        state.shi = random.randint(15, 20)
                        res["response"][
                            "text"] = f"Вы выбросили {state.shi}, чтобы узнать пробили ли вы щит скажите 'продолжить'"
                        state.fight_step = 3
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы пробить щит скажите 'пробить щит'"
                elif state.fight_step == 3:
                    if req["request"]["original_utterance"].lower() in ["продолжить", "дальше"]:
                        if state.shi >= state.stateen["enemshi"]:
                            res["response"]["text"] = "Вы пробили щит, теперь бросьте кубик урона, чтобы это сделать " \
                                                      "скажите 'нанести урон'"
                            state.fight_step = 4
                        else:
                            res["response"][
                                "text"] = "Вы не пробили щит, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить'"
                elif state.fight_step == 4:
                    if req["request"]["original_utterance"].lower() in ["нанеси урон", "нанести урон"]:
                        state.atc = random.randint(state.state["mina"], state.state["maxa"])
                        state.stateen["enem_hp"] = state.stateen["enem_hp"] - state.atc
                        res["response"][
                            "text"] = f"теперь скажите, какую атаку вы хотите использовать один два или три, \n" \
                                      f"чтобы посмотреть атаки, скажите 'способности мага'"
                        state.fight_step = 5
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы нанести урон скажите 'нанести урон'"
                elif state.fight_step == 5:
                    if req["request"]["original_utterance"].lower() in ["1", "первая", "один"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"]["text"] = f"Вы испепелили злобного дракона, чтобы получить награду, скажите 'получить награду'"
                            res["response"]["tts"] = f'<speaker audio="alice-sounds-game-win-3.opus"> Вы испепелили злобного дракона, ' \
                                                     f'чтобы получить награду, скажите "получить награду"'
                            state.fights = 1
                            state.fight_step = 1
                            state.etap = 'ending'
                    elif req["request"]["original_utterance"].lower() in ["2", "вторая", "два"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"]["text"] = f"Вы нанесли {state.atc} урона дракону, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"]["text"] = f"Вы уничтожили злобного дракона энергосферой, чтобы получить награду, скажите 'получить награду'"
                            res["response"]["tts"] = f'<speaker audio="alice-sounds-game-win-3.opus"> Вы уничтожили злобного' \
                                                     f' дракона энергосферой, чтобы получить награду, скажите "получить награду"'
                            state.fights = 1
                            state.fight_step = 1
                            state.etap = 'ending'
                    elif req["request"]["original_utterance"].lower() in ["3", "третья", "три"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"]["text"] = f"Вы разорвали дракона с помощью теликинеза, чтобы получить награду, скажите 'получить награду'"
                            res["response"]["tts"] = f'<speaker audio="alice-sounds-game-win-3.opus"> Вы разорвали дракона ' \
                                                     f'с помощью теликинеза, чтобы получить награду, скажите "получить награду"'
                            state.fights = 1
                            state.fight_step = 1
                            state.etap = 'ending'
                    else:
                        res["response"]["text"] = f"скажите, какую атаку вы хотите использовать один два или три, \n" \
                                                  f"чтобы посмотреть атаки, скажите 'способности мага'"

                elif state.fight_step == -1:
                    if req["request"]["original_utterance"].lower() in ["продолжить", "дальше"]:
                        enem_atc = random.randint(state.stateen["enemmaxa"], state.stateen["enemmina"])
                        enem_atsh = random.randint(15, 20)
                        if enem_atsh >= state.state["shield"] and (state.state["hp"] + enem_atc) > 0:
                            res["response"]["text"] = f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                                      f"урона, теперь кидайте кубик щита" \
                                                      f" напоминаю, чтобы пробить щит скажите 'пробить щит'"
                            state.state["hp"] = state.state["hp"] + enem_atc
                            state.fight_step = 2
                        elif enem_atsh >= state.state["shield"] and (state.state["hp"] + enem_atc) <= 0:
                            res["response"]["text"] = f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                                      f"урона, и к сожалению вы погибли..." \
                                                      f" захотите поиграть еще, я всегда тут"
                            res["response"]["tts"] = f'<speaker audio="alice-sounds-game-loss-3.opus">'\
                                                      f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                                      f"урона, и к сожалению вы погибли..." \
                                                      f" захотите поиграть еще, я всегда тут"
                            res['response']['end_session'] = True
                            state.state = {}
                            state.etap = "askname"
                            state.fights = 0
                            state.fight_step = 1
                            state.num = [1, 3, 4, 6, 7, 8, 9, 10, 11, 13]

                        else:
                            res["response"]["text"] = f"Враг выбросил {enem_atsh} и не пробил ваш щит теперь вы кидаете кубик щита" \
                                                      f" напоминаю, чтобы пробить щит скажите 'пробить щит'"
                            state.fight_step = 2
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить'"

            elif state.fights == 2:
                n = random.choice(state.num)
                wizard2 = db_sess.query(Wizard).filter(Wizard.id == n).first()
                if state.fight_step == 1:
                    state.stateen["enem_hp"] = wizard2.enemyhp
                    state.stateen["enem"] = wizard2.enemy
                    state.stateen["enemshi"] = wizard2.shield
                    state.stateen["enemmina"] = wizard2.minatack
                    state.stateen["enemmaxa"] = wizard2.maxatack
                    state.stateen["enemfirst"] = wizard2.firstkill
                    state.stateen["enemsecond"] = wizard2.secondkill
                    state.stateen["enemthird"] = wizard2.thirdkill
                    if req["request"]["original_utterance"].lower() in ["продолжить приключение", "продолжи приключение"]:
                        res["response"]["text"] = f"Вы наткнулись на {state.stateen['enem']}\n" \
                                                  f"Параметры врага:\n" \
                                                  f"хп: {state.stateen['enem_hp']}\n" \
                                                  f"щит: {state.stateen['enemshi']}\n" \
                                                  f"минимальная атака: {state.stateen['enemmina']}\n" \
                                                  f"максимальная атака: {state.stateen['enemmaxa']}\n" \
                                                  f"Чтобы ударить врага пробейте его щит, скажите 'пробить щит'"
                        state.fight_step = 2

                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить приключение'"
                elif state.fight_step == 2:
                    if req["request"]["original_utterance"].lower() in ["пробей щит", "пробить щит"]:
                        state.shi = random.randint(15, 20)
                        res["response"][
                            "text"] = f"Вы выбросили {state.shi}, чтобы узнать пробили ли вы щит скажите 'продолжить'"
                        state.fight_step = 3
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы пробить щит скажите 'пробить щит'"
                elif state.fight_step == 3:
                    if req["request"]["original_utterance"].lower() in ["продолжить", "дальше"]:
                        if state.shi >= state.stateen["enemshi"]:
                            res["response"]["text"] = "Вы пробили щит, теперь бросьте кубик урона, чтобы это сделать " \
                                                      "скажите 'нанести урон'"
                            state.fight_step = 4
                        else:
                            res["response"][
                                "text"] = "Вы не пробили щит, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить'"
                elif state.fight_step == 4:
                    if req["request"]["original_utterance"].lower() in ["нанеси урон", "нанести урон"]:
                        state.atc = random.randint(state.state["mina"], state.state["maxa"])
                        state.stateen["enem_hp"] = state.stateen["enem_hp"] - state.atc
                        res["response"][
                            "text"] = f"теперь скажите, какую атаку вы хотите использовать один два или три, \n" \
                                      f"чтобы посмотреть атаки, скажите 'способности мага'"
                        state.fight_step = 5
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы нанести урон скажите 'нанести урон'"
                elif state.fight_step == 5:
                    if req["request"]["original_utterance"].lower() in ["1", "первая", "один"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"][
                                "text"] = f"{state.stateen['enemfirst']}. Вы узнали, что в вашем королевстве беда! Казну обокрал " \
                                          f"дракон, чтобы найти логово дракона, скажите 'найти дракона'"
                            state.fights = 3
                            state.fight_step = 1
                            state.num.remove(n)
                    elif req["request"]["original_utterance"].lower() in ["2", "вторая", "два"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"][
                                "text"] = f"{state.stateen['enemsecond']}. Вы узнали, что в вашем королевстве беда! Казну обокрал " \
                                          f"дракон, чтобы найти логово дракона, скажите 'найти дракона'"
                            state.fights = 3
                            state.fight_step = 1
                            state.num.remove(n)
                    elif req["request"]["original_utterance"].lower() in ["3", "третья", "три"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"][
                                "text"] = f"{state.stateen['enemthird']}. Вы узнали, что в вашем королевстве беда! Казну обокрал " \
                                          f"дракон, чтобы найти логово дракона, скажите 'найти дракона'"
                            state.fights = 3
                            state.fight_step = 1
                            state.num.remove(n)
                    else:
                        res["response"]["text"] = f"скажите, какую атаку вы хотите использовать один два или три, \n" \
                                                  f"чтобы посмотреть атаки, скажите 'способности мага'"

                elif state.fight_step == -1:
                    if req["request"]["original_utterance"].lower() in ["продолжить", "дальше"]:
                        enem_atc = random.randint(state.stateen["enemmaxa"], state.stateen["enemmina"])
                        enem_atsh = random.randint(15, 20)
                        if enem_atsh >= state.state["shield"] and (state.state["hp"] + enem_atc) > 0:
                            res["response"]["text"] = f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                                      f"урона, теперь кидайте кубик щита" \
                                                      f" напоминаю, чтобы пробить щит скажите 'пробить щит'"
                            state.state["hp"] = state.state["hp"] + enem_atc
                            state.fight_step = 2
                        elif enem_atsh >= state.state["shield"] and (state.state["hp"] + enem_atc) <= 0:
                            res["response"]["text"] = f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                                      f"урона, и к сожалению вы погибли..." \
                                                      f" захотите поиграть еще, я всегда тут"
                            res["response"]["tts"] = f'<speaker audio="alice-sounds-game-loss-3.opus">'\
                                                      f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                                      f"урона, и к сожалению вы погибли..." \
                                                      f" захотите поиграть еще, я всегда тут"
                            res['response']['end_session'] = True
                            state.state = {}
                            state.etap = "askname"
                            state.fights = 0
                            state.fight_step = 1
                            state.num = [1, 3, 4, 6, 7, 8, 9, 10, 11, 13]

                        else:
                            res["response"]["text"] = f"Враг выбросил {enem_atsh} и не пробил ваш щит теперь вы кидаете кубик щита" \
                                                      f" напоминаю, чтобы пробить щит скажите 'пробить щит'"
                            state.fight_step = 2
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить'"

            elif state.fights == 1:
                n = random.choice(state.num)
                wizard1 = db_sess.query(Wizard).filter(Wizard.id == n).first()
                if state.fight_step == 1:
                    state.stateen["enem_hp"] = wizard1.enemyhp
                    state.stateen["enem"] = wizard1.enemy
                    state.stateen["enemshi"] = wizard1.shield
                    state.stateen["enemmina"] = wizard1.minatack
                    state.stateen["enemmaxa"] = wizard1.maxatack
                    state.stateen["enemfirst"] = wizard1.firstkill
                    state.stateen["enemsecond"] = wizard1.secondkill
                    state.stateen["enemthird"] = wizard1.thirdkill
                    if req["request"]["original_utterance"].lower() in ["продолжить приключение", "продолжи приключение"]:
                        res["response"]["text"] = f"Вы наткнулись на {state.stateen['enem']}\n" \
                                                  f"Параметры врага:\n" \
                                                  f"хп: {state.stateen['enem_hp']}\n" \
                                                  f"щит: {state.stateen['enemshi']}\n" \
                                                  f"минимальная атака: {state.stateen['enemmina']}\n" \
                                                  f"максимальная атака: {state.stateen['enemmaxa']}\n" \
                                                  f"Чтобы ударить врага пробейте его щит, скажите 'пробить щит'"
                        state.fight_step = 2

                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить приключение'"
                elif state.fight_step == 2:
                    if req["request"]["original_utterance"].lower() in ["пробить щит", "пробей щит"]:
                        state.shi = random.randint(15, 20)
                        res["response"][
                            "text"] = f"Вы выбросили {state.shi}, чтобы узнать пробили ли вы щит скажите 'продолжить'"
                        state.fight_step = 3
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы пробить щит скажите 'пробить щит'"
                elif state.fight_step == 3:
                    if req["request"]["original_utterance"].lower() in ["продолжить", "дальше"]:
                        if state.shi >= state.stateen["enemshi"]:
                            res["response"]["text"] = "Вы пробили щит, теперь бросьте кубик урона, чтобы это сделать " \
                                                      "скажите 'нанести урон'"
                            state.fight_step = 4
                        else:
                            res["response"][
                                "text"] = "Вы не пробили щит, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить'"
                elif state.fight_step == 4:
                    if req["request"]["original_utterance"].lower() in ["нанеси урон", "нанести урон"]:
                        state.atc = random.randint(state.state["mina"], state.state["maxa"])
                        state.stateen["enem_hp"] = state.stateen["enem_hp"] - state.atc
                        res["response"][
                            "text"] = f"теперь скажите, какую атаку вы хотите использовать один два или три, \n" \
                                      f"чтобы посмотреть атаки, скажите 'способности мага'"
                        state.fight_step = 5
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы нанести урон скажите 'нанести урон'"
                elif state.fight_step == 5:
                    if req["request"]["original_utterance"].lower() in ["1", "первая", "один"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"][
                                "text"] = f"{state.stateen['enemfirst']}, чтобы продолжить, скажите 'продолжить приключение'"
                            state.fights = 2
                            state.fight_step = 1
                            state.num.remove(n)
                    elif req["request"]["original_utterance"].lower() in ["2", "вторая", "два"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"][
                                "text"] = f"{state.stateen['enemsecond']}, чтобы продолжить, скажите 'продолжить приключение'"
                            state.fights = 2
                            state.fight_step = 1
                            state.num.remove(n)
                    elif req["request"]["original_utterance"].lower() in ["3", "третья", "три"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"][
                                "text"] = f"{state.stateen['enemthird']}, чтобы продолжить, скажите 'продолжить приключение'"
                            state.fights = 2
                            state.fight_step = 1
                            state.num.remove(n)
                    else:
                        res["response"]["text"] = f"скажите, какую атаку вы хотите использовать один два или три, \n" \
                                                  f"чтобы посмотреть атаки, скажите 'способности мага'"

                elif state.fight_step == -1:
                    if req["request"]["original_utterance"].lower() in ["продолжить", "дальше"]:
                        enem_atc = random.randint(state.stateen["enemmaxa"], state.stateen["enemmina"])
                        enem_atsh = random.randint(15, 20)
                        if enem_atsh >= state.state["shield"] and (state.state["hp"] + enem_atc) > 0:
                            res["response"]["text"] = f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                                      f"урона, теперь кидайте кубик щита" \
                                                      f" напоминаю, чтобы пробить щит скажите 'пробить щит'"
                            state.state["hp"] = state.state["hp"] + enem_atc
                            state.fight_step = 2
                        elif enem_atsh >= state.state["shield"] and (state.state["hp"] + enem_atc) <= 0:
                            res["response"]["text"] = f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                                      f"урона, и к сожалению вы погибли..." \
                                                      f" захотите поиграть еще, я всегда тут"
                            res["response"]["tts"] = f'<speaker audio="alice-sounds-game-loss-3.opus">'\
                                                      f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                                      f"урона, и к сожалению вы погибли..." \
                                                      f" захотите поиграть еще, я всегда тут"
                            res['response']['end_session'] = True
                            state.state = {}
                            state.etap = "askname"
                            state.fights = 0
                            state.fight_step = 1
                            state.num = [1, 3, 4, 6, 7, 8, 9, 10, 11, 13]

                        else:
                            res["response"]["text"] = f"Враг выбросил {enem_atsh} и не пробил ваш щит теперь вы кидаете кубик щита" \
                                                      f" напоминаю, чтобы пробить щит скажите 'пробить щит'"
                            state.fight_step = 2
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить'"

            elif state.fights == 0:
                n = random.choice(state.num)
                wizard0 = db_sess.query(Wizard).filter(Wizard.id == n).first()
                if state.fight_step == 1:
                    state.stateen["enem_hp"] = wizard0.enemyhp
                    state.stateen["enem"] = wizard0.enemy
                    state.stateen["enemshi"] = wizard0.shield
                    state.stateen["enemmina"] = wizard0.minatack
                    state.stateen["enemmaxa"] = wizard0.maxatack
                    state.stateen["enemfirst"] = wizard0.firstkill
                    state.stateen["enemsecond"] = wizard0.secondkill
                    state.stateen["enemthird"] = wizard0.thirdkill
                    if req["request"]["original_utterance"].lower() in ["начать приключение", "начни приключение"]:
                        res["response"]["text"] = f"Вы наткнулись на {state.stateen['enem']}\n" \
                                                  f"Параметры врага:\n" \
                                                  f"хп: {state.stateen['enem_hp']}\n" \
                                                  f"щит: {state.stateen['enemshi']}\n" \
                                                  f"минимальная атака: {state.stateen['enemmina']}\n" \
                                                  f"максимальная атака: {state.stateen['enemmaxa']}\n" \
                                                  f"Чтобы ударить врага пробейте его щит, скажите 'пробить щит'"
                        state.fight_step = 2

                    else:
                        res["response"]["text"] = "Напоминаю, чтобы начать скажите 'начать приключение'"
                elif state.fight_step == 2:
                    if req["request"]["original_utterance"].lower() in ["пробей щит", "пробить щит"]:
                        state.shi = random.randint(15, 20)
                        res["response"]["text"] = f"Вы выбросили {state.shi}, чтобы узнать пробили ли вы щит скажите 'продолжить'"
                        state.fight_step = 3
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы пробить щит скажите 'пробить щит'"
                elif state.fight_step == 3:
                    if req["request"]["original_utterance"].lower() in ["продолжить", "дальше"]:
                        if state.shi >= state.stateen["enemshi"]:
                            res["response"]["text"] = "Вы пробили щит, теперь бросьте кубик урона, чтобы это сделать " \
                                                      "скажите 'нанести урон'"
                            state.fight_step = 4
                        else:
                            res["response"]["text"] = "Вы не пробили щит, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить'"
                elif state.fight_step == 4:
                    if req["request"]["original_utterance"].lower() in ["нанеси урон", "нанести урон"]:
                        state.atc = random.randint(state.state["mina"], state.state["maxa"])
                        state.stateen["enem_hp"] = state.stateen["enem_hp"] - state.atc
                        res["response"]["text"] = f"теперь скажите, какую атаку вы хотите использовать один два или три, \n" \
                                                  f"чтобы посмотреть атаки, скажите 'способности мага'"
                        state.fight_step = 5
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы нанести урон скажите 'нанести урон'"
                elif state.fight_step == 5:
                    if req["request"]["original_utterance"].lower() in ["1", "первая", "один"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"]["text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"]["text"] = f"{state.stateen['enemfirst']}, чтобы продолжить, скажите 'продолжить приключение'"
                            state.fights = 1
                            state.fight_step = 1
                            state.num.remove(n)
                    elif req["request"]["original_utterance"].lower() in ["2", "вторая", "два"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"]["text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"]["text"] = f"{state.stateen['enemsecond']}, чтобы продолжить, скажите 'продолжить приключение'"
                            state.fights = 1
                            state.fight_step = 1
                            state.num.remove(n)
                    elif req["request"]["original_utterance"].lower() in ["3", "третья", "три"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"]["text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"]["text"] = f"{state.stateen['enemthird']}, чтобы продолжить, скажите 'продолжить приключение'"
                            state.fights = 1
                            state.fight_step = 1
                            state.num.remove(n)
                    else:
                        res["response"]["text"] = f"скажите, какую атаку вы хотите использовать один два или три, \n" \
                                                  f"чтобы посмотреть атаки, скажите 'способности мага'"

                elif state.fight_step == -1:
                    if req["request"]["original_utterance"].lower() in ["продолжить", "дальше"]:
                        enem_atc = random.randint(state.stateen["enemmaxa"], state.stateen["enemmina"])
                        enem_atsh = random.randint(15, 20)
                        if enem_atsh >= state.state["shield"] and (state.state["hp"] + enem_atc) > 0:
                            res["response"]["text"] = f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                                      f"урона, теперь кидайте кубик щита" \
                                                      f" напоминаю, чтобы пробить щит скажите 'пробить щит'"
                            state.state["hp"] = state.state["hp"] + enem_atc
                            state.fight_step = 2
                        elif enem_atsh >= state.state["shield"] and (state.state["hp"] + enem_atc) <= 0:
                            res["response"]["text"] = f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                                      f"урона, и к сожалению вы погибли..." \
                                                      f" захотите поиграть еще, я всегда тут"
                            res["response"]["tts"] = f'<speaker audio="alice-sounds-game-loss-3.opus">'\
                                                      f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                                      f"урона, и к сожалению вы погибли..." \
                                                      f" захотите поиграть еще, я всегда тут"
                            res['response']['end_session'] = True
                            state.state = {}
                            state.etap = "askname"
                            state.fights = 0
                            state.fight_step = 1
                            state.num = [1, 3, 4, 6, 7, 8, 9, 10, 11, 13]

                        else:
                            res["response"]["text"] = f"Враг выбросил {enem_atsh} и не пробил ваш щит теперь вы кидаете кубик щита" \
                                                      f" напоминаю, чтобы пробить щит скажите 'пробить щит'"
                            state.fight_step = 2
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить'"

        elif state.state["role"] == "эльф":
            if state.fights == 3:
                n = 12
                elf3 = db_sess.query(Elf).filter(Elf.id == n).first()
                if state.fight_step == 1:
                    state.stateen["enem_hp"] = elf3.enemyhp
                    state.stateen["enem"] = elf3.enemy
                    state.stateen["enemshi"] = elf3.shield
                    state.stateen["enemmina"] = elf3.minatack
                    state.stateen["enemmaxa"] = elf3.maxatack
                    state.stateen["enemfirst"] = elf3.firstkill
                    state.stateen["enemsecond"] = elf3.secondkill
                    state.stateen["enemthird"] = elf3.thirdkill
                    if req["request"]["original_utterance"].lower() in ["найти дракона", "искать дракона"]:
                        res["response"]["text"] = f"Вы встретили огромного дракона, сторожащего золото\n" \
                                                  f"Параметры дракона:\n" \
                                                  f"хп: {state.stateen['enem_hp']}\n" \
                                                  f"щит: {state.stateen['enemshi']}\n" \
                                                  f"минимальная атака: {state.stateen['enemmina']}\n" \
                                                  f"максимальная атака: {state.stateen['enemmaxa']}\n" \
                                                  f"Чтобы ударить дракона пробейте его щит, скажите 'пробить щит'"
                        state.fight_step = 2

                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить приключение'"
                elif state.fight_step == 2:
                    if req["request"]["original_utterance"].lower() in ["пробей щит", "пробить щит"]:
                        state.shi = random.randint(15, 20)
                        res["response"][
                            "text"] = f"Вы выбросили {state.shi}, чтобы узнать пробили ли вы щит скажите 'продолжить'"
                        state.fight_step = 3
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы пробить щит скажите 'пробить щит'"
                elif state.fight_step == 3:
                    if req["request"]["original_utterance"].lower() in ["продолжить", "дальше"]:
                        if state.shi >= state.stateen["enemshi"]:
                            res["response"]["text"] = "Вы пробили щит, теперь бросьте кубик урона, чтобы это сделать " \
                                                      "скажите 'нанести урон'"
                            state.fight_step = 4
                        else:
                            res["response"][
                                "text"] = "Вы не пробили щит, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить'"
                elif state.fight_step == 4:
                    if req["request"]["original_utterance"].lower() in ["нанеси урон", "нанести урон"]:
                        state.atc = random.randint(state.state["mina"], state.state["maxa"])
                        state.stateen["enem_hp"] = state.stateen["enem_hp"] - state.atc
                        res["response"][
                            "text"] = f"теперь скажите, какую атаку вы хотите использовать один два или три, \n" \
                                      f"чтобы посмотреть атаки, скажите 'способности эльфа'"
                        state.fight_step = 5
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы нанести урон скажите 'нанести урон'"
                elif state.fight_step == 5:
                    if req["request"]["original_utterance"].lower() in ["1", "первая", "один"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"]["text"] = f"Вы попали дракону в сердце, чтобы получить награду, скажите 'получить награду'"
                            res["response"]["tts"] = f'<speaker audio="alice-sounds-game-win-3.opus"> Вы попали дракону в' \
                                                     f' сердце, чтобы получить награду, скажите "получить награду"'
                            state.fights = 1
                            state.fight_step = 1
                            state.etap = 'ending'
                    elif req["request"]["original_utterance"].lower() in ["2", "вторая", "два"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона дракону, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"]["text"] = f"Вы задушили дракона, чтобы получить награду, скажите 'получить награду'"
                            res["response"]["tts"] = f'<speaker audio="alice-sounds-game-win-3.opus"> Вы задушили дракона,' \
                                                     f' чтобы получить награду, скажите "получить награду"'
                            state.fights = 1
                            state.fight_step = 1
                            state.etap = 'ending'
                    elif req["request"]["original_utterance"].lower() in ["3", "третья", "три"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"]["text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"]["text"] = f"Вы кинули кинжал дракону прямо в сердце, чтобы получить награду, скажите 'получить награду'"
                            res["response"]["tts"] = f'<speaker audio="alice-sounds-game-win-3.opus"> Вы кинули кинжал ' \
                                                     f'дракону прямо в сердце, чтобы получить награду, скажите "получить награду"'
                            state.fights = 1
                            state.fight_step = 1
                            state.etap = 'ending'
                    else:
                        res["response"]["text"] = f"скажите, какую атаку вы хотите использовать один два или три, \n" \
                                                  f"чтобы посмотреть атаки, скажите 'способности эльфа'"

                elif state.fight_step == -1:
                    if req["request"]["original_utterance"].lower() in ["продолжить", "дальше"]:
                        enem_atc = random.randint(state.stateen["enemmaxa"], state.stateen["enemmina"])
                        enem_atsh = random.randint(15, 20)
                        if enem_atsh >= state.state["shield"] and (state.state["hp"] + enem_atc) > 0:
                            res["response"][
                                "text"] = f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                          f"урона, теперь кидайте кубик щита" \
                                          f" напоминаю, чтобы пробить щит скажите 'пробить щит'"
                            state.state["hp"] = state.state["hp"] + enem_atc
                            state.fight_step = 2
                        elif enem_atsh >= state.state["shield"] and (state.state["hp"] + enem_atc) <= 0:
                            res["response"][
                                "text"] = f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                          f"урона, и к сожалению вы погибли..." \
                                          f" захотите поиграть еще, я всегда тут"
                            res["response"]["tts"] = f'<speaker audio="alice-sounds-game-loss-3.opus">'\
                                                      f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                                      f"урона, и к сожалению вы погибли..." \
                                                      f" захотите поиграть еще, я всегда тут"
                            res['response']['end_session'] = True
                            state.state = {}
                            state.etap = "askname"
                            state.fights = 0
                            state.fight_step = 1
                            state.num = [1, 3, 4, 6, 7, 8, 9, 10, 11, 13]

                        else:
                            res["response"][
                                "text"] = f"Враг выбросил {enem_atsh} и не пробил ваш щит теперь вы кидаете кубик щита" \
                                          f" напоминаю, чтобы пробить щит скажите 'пробить щит'"
                            state.fight_step = 2
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить'"

            elif state.fights == 2:
                n = random.choice(state.num)
                elf2 = db_sess.query(Elf).filter(Elf.id == n).first()
                if state.fight_step == 1:
                    state.stateen["enem_hp"] = elf2.enemyhp
                    state.stateen["enem"] = elf2.enemy
                    state.stateen["enemshi"] = elf2.shield
                    state.stateen["enemmina"] = elf2.minatack
                    state.stateen["enemmaxa"] = elf2.maxatack
                    state.stateen["enemfirst"] = elf2.firstkill
                    state.stateen["enemsecond"] = elf2.secondkill
                    state.stateen["enemthird"] = elf2.thirdkill
                    if req["request"]["original_utterance"].lower() in ["продолжить приключение", "продолжи приключение"]:
                        res["response"]["text"] = f"Вы наткнулись на {state.stateen['enem']}\n" \
                                                  f"Параметры врага:\n" \
                                                  f"хп: {state.stateen['enem_hp']}\n" \
                                                  f"щит: {state.stateen['enemshi']}\n" \
                                                  f"минимальная атака: {state.stateen['enemmina']}\n" \
                                                  f"максимальная атака: {state.stateen['enemmaxa']}\n" \
                                                  f"Чтобы ударить врага пробейте его щит, скажите 'пробить щит'"
                        state.fight_step = 2

                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить приключение'"
                elif state.fight_step == 2:
                    if req["request"]["original_utterance"].lower() in ["пробей щит", "пробить щит"]:
                        state.shi = random.randint(15, 20)
                        res["response"][
                            "text"] = f"Вы выбросили {state.shi}, чтобы узнать пробили ли вы щит скажите 'продолжить'"
                        state.fight_step = 3
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы пробить щит скажите 'пробить щит'"
                elif state.fight_step == 3:
                    if req["request"]["original_utterance"].lower() in ["продолжить", "дальше"]:
                        if state.shi >= state.stateen["enemshi"]:
                            res["response"]["text"] = "Вы пробили щит, теперь бросьте кубик урона, чтобы это сделать " \
                                                      "скажите 'нанести урон'"
                            state.fight_step = 4
                        else:
                            res["response"][
                                "text"] = "Вы не пробили щит, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить'"
                elif state.fight_step == 4:
                    if req["request"]["original_utterance"].lower() in ["нанеси урон", "нанести урон"]:
                        state.atc = random.randint(state.state["mina"], state.state["maxa"])
                        state.stateen["enem_hp"] = state.stateen["enem_hp"] - state.atc
                        res["response"][
                            "text"] = f"теперь скажите, какую атаку вы хотите использовать один два или три, \n" \
                                      f"чтобы посмотреть атаки, скажите 'способности эльфа'"
                        state.fight_step = 5
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы нанести урон скажите 'нанести урон'"
                elif state.fight_step == 5:
                    if req["request"]["original_utterance"].lower() in ["1", "первая", "один"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"][
                                "text"] = f"{state.stateen['enemfirst']}. Вы узнали, что в вашем королевстве беда! Казну обокрал " \
                                          f"дракон, чтобы найти логово дракона, скажите 'найти дракона'"
                            state.fights = 3
                            state.fight_step = 1
                            state.num.remove(n)
                    elif req["request"]["original_utterance"].lower() in ["2", "вторая", "два"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"][
                                "text"] = f"{state.stateen['enemsecond']}. Вы узнали, что в вашем королевстве беда! Казну обокрал " \
                                          f"дракон, чтобы найти логово дракона, скажите 'найти дракона'"
                            state.fights = 3
                            state.fight_step = 1
                            state.num.remove(n)
                    elif req["request"]["original_utterance"].lower() in ["3", "третья", "три"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"][
                                "text"] = f"{state.stateen['enemthird']}. Вы узнали, что в вашем королевстве беда! Казну обокрал " \
                                          f"дракон, чтобы найти логово дракона, скажите 'найти дракона'"
                            state.fights = 3
                            state.fight_step = 1
                            state.num.remove(n)
                    else:
                        res["response"]["text"] = f"скажите, какую атаку вы хотите использовать один два или три, \n" \
                                                  f"чтобы посмотреть атаки, скажите 'способности эльфа'"

                elif state.fight_step == -1:
                    if req["request"]["original_utterance"].lower() in ["продолжить", "дальше"]:
                        enem_atc = random.randint(state.stateen["enemmaxa"], state.stateen["enemmina"])
                        enem_atsh = random.randint(15, 20)
                        if enem_atsh >= state.state["shield"] and (state.state["hp"] + enem_atc) > 0:
                            res["response"][
                                "text"] = f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                          f"урона, теперь кидайте кубик щита" \
                                          f" напоминаю, чтобы пробить щит скажите 'пробить щит'"
                            state.state["hp"] = state.state["hp"] + enem_atc
                            state.fight_step = 2
                        elif enem_atsh >= state.state["shield"] and (state.state["hp"] + enem_atc) <= 0:
                            res["response"][
                                "text"] = f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                          f"урона, и к сожалению вы погибли..." \
                                          f" захотите поиграть еще, я всегда тут"
                            res["response"]["tts"] = f'<speaker audio="alice-sounds-game-loss-3.opus">'\
                                                      f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                                      f"урона, и к сожалению вы погибли..." \
                                                      f" захотите поиграть еще, я всегда тут"
                            res['response']['end_session'] = True
                            state.state = {}
                            state.etap = "askname"
                            state.fights = 0
                            state.fight_step = 1
                            state.num = [1, 3, 4, 6, 7, 8, 9, 10, 11, 13]

                        else:
                            res["response"][
                                "text"] = f"Враг выбросил {enem_atsh} и не пробил ваш щит теперь вы кидаете кубик щита" \
                                          f" напоминаю, чтобы пробить щит скажите 'пробить щит'"
                            state.fight_step = 2
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить'"

            elif state.fights == 1:
                n = random.choice(state.num)
                elf1 = db_sess.query(Elf).filter(Elf.id == n).first()
                if state.fight_step == 1:
                    state.stateen["enem_hp"] = elf1.enemyhp
                    state.stateen["enem"] = elf1.enemy
                    state.stateen["enemshi"] = elf1.shield
                    state.stateen["enemmina"] = elf1.minatack
                    state.stateen["enemmaxa"] = elf1.maxatack
                    state.stateen["enemfirst"] = elf1.firstkill
                    state.stateen["enemsecond"] = elf1.secondkill
                    state.stateen["enemthird"] = elf1.thirdkill
                    if req["request"]["original_utterance"].lower() in ["продолжить приключение",
                                                                        "продолжи приключение"]:
                        res["response"]["text"] = f"Вы наткнулись на {state.stateen['enem']}\n" \
                                                  f"Параметры врага:\n" \
                                                  f"хп: {state.stateen['enem_hp']}\n" \
                                                  f"щит: {state.stateen['enemshi']}\n" \
                                                  f"минимальная атака: {state.stateen['enemmina']}\n" \
                                                  f"максимальная атака: {state.stateen['enemmaxa']}\n" \
                                                  f"Чтобы ударить врага пробейте его щит, скажите 'пробить щит'"
                        state.fight_step = 2

                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить приключение'"
                elif state.fight_step == 2:
                    if req["request"]["original_utterance"].lower() in ["пробей щит", "пробить щит"]:
                        state.shi = random.randint(15, 20)
                        res["response"][
                            "text"] = f"Вы выбросили {state.shi}, чтобы узнать пробили ли вы щит скажите 'продолжить'"
                        state.fight_step = 3
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы пробить щит скажите 'пробить щит'"
                elif state.fight_step == 3:
                    if req["request"]["original_utterance"].lower() in ["продолжить", "дальше"]:
                        if state.shi >= state.stateen["enemshi"]:
                            res["response"]["text"] = "Вы пробили щит, теперь бросьте кубик урона, чтобы это сделать " \
                                                      "скажите 'нанести урон'"
                            state.fight_step = 4
                        else:
                            res["response"][
                                "text"] = "Вы не пробили щит, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить'"
                elif state.fight_step == 4:
                    if req["request"]["original_utterance"].lower() in ["нанеси урон", "нанести урон"]:
                        state.atc = random.randint(state.state["mina"], state.state["maxa"])
                        state.stateen["enem_hp"] = state.stateen["enem_hp"] - state.atc
                        res["response"][
                            "text"] = f"теперь скажите, какую атаку вы хотите использовать один два или три, \n" \
                                      f"чтобы посмотреть атаки, скажите 'способности эльфа'"
                        state.fight_step = 5
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы нанести урон скажите 'нанести урон'"
                elif state.fight_step == 5:
                    if req["request"]["original_utterance"].lower() in ["1", "первая", "один"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"][
                                "text"] = f"{state.stateen['enemfirst']}, чтобы продолжить, скажите 'продолжить приключение'"
                            state.fights = 2
                            state.fight_step = 1
                            state.num.remove(n)
                    elif req["request"]["original_utterance"].lower() in ["2", "вторая", "два"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"][
                                "text"] = f"{state.stateen['enemsecond']}, чтобы продолжить, скажите 'продолжить приключение'"
                            state.fights = 2
                            state.fight_step = 1
                            state.num.remove(n)
                    elif req["request"]["original_utterance"].lower() in ["3", "третья", "три"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"][
                                "text"] = f"{state.stateen['enemthird']}, чтобы продолжить, скажите 'продолжить приключение'"
                            state.fights = 2
                            state.fight_step = 1
                            state.num.remove(n)
                    else:
                        res["response"]["text"] = f"скажите, какую атаку вы хотите использовать один два или три, \n" \
                                                  f"чтобы посмотреть атаки, скажите 'способности эльфа'"

                elif state.fight_step == -1:
                    if req["request"]["original_utterance"].lower() in ["продолжить", "дальше"]:
                        enem_atc = random.randint(state.stateen["enemmaxa"], state.stateen["enemmina"])
                        enem_atsh = random.randint(15, 20)
                        if enem_atsh >= state.state["shield"] and (state.state["hp"] + enem_atc) > 0:
                            res["response"][
                                "text"] = f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                          f"урона, теперь кидайте кубик щита" \
                                          f" напоминаю, чтобы пробить щит скажите 'пробить щит'"
                            state.state["hp"] = state.state["hp"] + enem_atc
                            state.fight_step = 2
                        elif enem_atsh >= state.state["shield"] and (state.state["hp"] + enem_atc) <= 0:
                            res["response"][
                                "text"] = f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                          f"урона, и к сожалению вы погибли..." \
                                          f" захотите поиграть еще, я всегда тут"
                            res["response"]["tts"] = f'<speaker audio="alice-sounds-game-loss-3.opus">'\
                                                      f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                                      f"урона, и к сожалению вы погибли..." \
                                                      f" захотите поиграть еще, я всегда тут"
                            res['response']['end_session'] = True
                            state.state = {}
                            state.etap = "askname"
                            state.fights = 0
                            state.fight_step = 1
                            state.num = [1, 3, 4, 6, 7, 8, 9, 10, 11, 13]

                        else:
                            res["response"][
                                "text"] = f"Враг выбросил {enem_atsh} и не пробил ваш щит теперь вы кидаете кубик щита" \
                                          f" напоминаю, чтобы пробить щит скажите 'пробить щит'"
                            state.fight_step = 2
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить'"

            elif state.fights == 0:
                n = random.choice(state.num)
                elf0 = db_sess.query(Elf).filter(Elf.id == n).first()
                if state.fight_step == 1:
                    state.stateen["enem_hp"] = elf0.enemyhp
                    state.stateen["enem"] = elf0.enemy
                    state.stateen["enemshi"] = elf0.shield
                    state.stateen["enemmina"] = elf0.minatack
                    state.stateen["enemmaxa"] = elf0.maxatack
                    state.stateen["enemfirst"] = elf0.firstkill
                    state.stateen["enemsecond"] = elf0.secondkill
                    state.stateen["enemthird"] = elf0.thirdkill
                    if req["request"]["original_utterance"].lower() in ["начать приключение", "начни приключение"]:
                        res["response"]["text"] = f"Вы наткнулись на {state.stateen['enem']}\n" \
                                                  f"Параметры врага:\n" \
                                                  f"хп: {state.stateen['enem_hp']}\n" \
                                                  f"щит: {state.stateen['enemshi']}\n" \
                                                  f"минимальная атака: {state.stateen['enemmina']}\n" \
                                                  f"максимальная атака: {state.stateen['enemmaxa']}\n" \
                                                  f"Чтобы ударить врага пробейте его щит, скажите 'пробить щит'"
                        state.fight_step = 2

                    else:
                        res["response"]["text"] = "Напоминаю, чтобы начать скажите 'начать приключение'"
                elif state.fight_step == 2:
                    if req["request"]["original_utterance"].lower() in ["пробей щит", "пробить щит"]:
                        state.shi = random.randint(15, 20)
                        res["response"][
                            "text"] = f"Вы выбросили {state.shi}, чтобы узнать пробили ли вы щит скажите 'продолжить'"
                        state.fight_step = 3
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы пробить щит скажите 'пробить щит'"
                elif state.fight_step == 3:
                    if req["request"]["original_utterance"].lower() in ["продолжить", "дальше"]:
                        if state.shi >= state.stateen["enemshi"]:
                            res["response"]["text"] = "Вы пробили щит, теперь бросьте кубик урона, чтобы это сделать " \
                                                      "скажите 'нанести урон'"
                            state.fight_step = 4
                        else:
                            res["response"][
                                "text"] = "Вы не пробили щит, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить'"
                elif state.fight_step == 4:
                    if req["request"]["original_utterance"].lower() in ["нанеси урон", "нанести урон"]:
                        state.atc = random.randint(state.state["mina"], state.state["maxa"])
                        state.stateen["enem_hp"] = state.stateen["enem_hp"] - state.atc
                        res["response"][
                            "text"] = f"теперь скажите, какую атаку вы хотите использовать один два или три, \n" \
                                      f"чтобы посмотреть атаки, скажите 'способности эльфа'"
                        state.fight_step = 5
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы нанести урон скажите 'нанести урон'"
                elif state.fight_step == 5:
                    if req["request"]["original_utterance"].lower() in ["1", "первая", "один"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"][
                                "text"] = f"{state.stateen['enemfirst']}, чтобы продолжить, скажите 'продолжить приключение'"
                            state.fights = 1
                            state.fight_step = 1
                            state.num.remove(n)
                    elif req["request"]["original_utterance"].lower() in ["2", "вторая", "два"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"][
                                "text"] = f"{state.stateen['enemsecond']}, чтобы продолжить, скажите 'продолжить приключение'"
                            state.fights = 1
                            state.fight_step = 1
                            state.num.remove(n)
                    elif req["request"]["original_utterance"].lower() in ["3", "третья", "три"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"][
                                "text"] = f"{state.stateen['enemthird']}, чтобы продолжить, скажите 'продолжить приключение'"
                            state.fights = 1
                            state.fight_step = 1
                            state.num.remove(n)
                    else:
                        res["response"]["text"] = f"скажите, какую атаку вы хотите использовать один два или три, \n" \
                                                  f"чтобы посмотреть атаки, скажите 'способности эльфа'"

                elif state.fight_step == -1:
                    if req["request"]["original_utterance"].lower() in ["продолжить", "дальше"]:
                        enem_atc = random.randint(state.stateen["enemmaxa"], state.stateen["enemmina"])
                        enem_atsh = random.randint(15, 20)
                        if enem_atsh >= state.state["shield"] and (state.state["hp"] + enem_atc) > 0:
                            res["response"][
                                "text"] = f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                          f"урона, теперь кидайте кубик щита" \
                                          f" напоминаю, чтобы пробить щит скажите 'пробить щит'"
                            state.state["hp"] = state.state["hp"] + enem_atc
                            state.fight_step = 2
                        elif enem_atsh >= state.state["shield"] and (state.state["hp"] + enem_atc) <= 0:
                            res["response"][
                                "text"] = f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                          f"урона, и к сожалению вы погибли..." \
                                          f" захотите поиграть еще, я всегда тут"
                            res["response"]["tts"] = f'<speaker audio="alice-sounds-game-loss-3.opus">'\
                                                      f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                                      f"урона, и к сожалению вы погибли..." \
                                                      f" захотите поиграть еще, я всегда тут"
                            res['response']['end_session'] = True
                            state.state = {}
                            state.etap = "askname"
                            state.fights = 0
                            state.fight_step = 1
                            state.num = [1, 3, 4, 6, 7, 8, 9, 10, 11, 13]

                        else:
                            res["response"][
                                "text"] = f"Враг выбросил {enem_atsh} и не пробил ваш щит теперь вы кидаете кубик щита" \
                                          f" напоминаю, чтобы пробить щит скажите 'пробить щит'"
                            state.fight_step = 2
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить'"

        elif state.state["role"] == "варвар":
            if state.fights == 3:
                n = 12
                barbarian3 = db_sess.query(Barbarian).filter(Barbarian.id == n).first()
                if state.fight_step == 1:
                    state.stateen["enem_hp"] = barbarian3.enemyhp
                    state.stateen["enem"] = barbarian3.enemy
                    state.stateen["enemshi"] = barbarian3.shield
                    state.stateen["enemmina"] = barbarian3.minatack
                    state.stateen["enemmaxa"] = barbarian3.maxatack
                    state.stateen["enemfirst"] = barbarian3.firstkill
                    state.stateen["enemsecond"] = barbarian3.secondkill
                    state.stateen["enemthird"] = barbarian3.thirdkill
                    if req["request"]["original_utterance"].lower() in ["найти дракона", "искать дракона"]:
                        res["response"]["text"] = f"Вы встретили огромного дракона, сторожащего золото\n" \
                                                  f"Параметры дракона:\n" \
                                                  f"хп: {state.stateen['enem_hp']}\n" \
                                                  f"щит: {state.stateen['enemshi']}\n" \
                                                  f"минимальная атака: {state.stateen['enemmina']}\n" \
                                                  f"максимальная атака: {state.stateen['enemmaxa']}\n" \
                                                  f"Чтобы ударить дракона пробейте его щит, скажите 'пробить щит'"
                        state.fight_step = 2

                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить приключение'"
                elif state.fight_step == 2:
                    if req["request"]["original_utterance"].lower() in ["пробей щит", "пробить щит"]:
                        state.shi = random.randint(15, 20)
                        res["response"][
                            "text"] = f"Вы выбросили {state.shi}, чтобы узнать пробили ли вы щит скажите 'продолжить'"
                        state.fight_step = 3
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы пробить щит скажите 'пробить щит'"
                elif state.fight_step == 3:
                    if req["request"]["original_utterance"].lower() in ["продолжить", "дальше"]:
                        if state.shi >= state.stateen["enemshi"]:
                            res["response"]["text"] = "Вы пробили щит, теперь бросьте кубик урона, чтобы это сделать " \
                                                      "скажите 'нанести урон'"
                            state.fight_step = 4
                        else:
                            res["response"][
                                "text"] = "Вы не пробили щит, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить'"
                elif state.fight_step == 4:
                    if req["request"]["original_utterance"].lower() in ["нанеси урон", "нанести урон"]:
                        state.atc = random.randint(state.state["mina"], state.state["maxa"])
                        state.stateen["enem_hp"] = state.stateen["enem_hp"] - state.atc
                        res["response"][
                            "text"] = f"теперь скажите, какую атаку вы хотите использовать один два или три, \n" \
                                      f"чтобы посмотреть атаки, скажите 'способности варвара'"
                        state.fight_step = 5
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы нанести урон скажите 'нанести урон'"
                elif state.fight_step == 5:
                    if req["request"]["original_utterance"].lower() in ["1", "первая", "один"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"]["text"] = f"Вы отрубили голову дракону, чтобы получить награду, скажите 'получить награду'"
                            res["response"]["tts"] = f'<speaker audio="alice-sounds-game-win-3.opus"> Вы отрубили голову' \
                                                     f' дракону, чтобы получить награду, скажите "получить награду"'
                            state.fights = 1
                            state.fight_step = 1
                            state.etap = 'ending'
                    elif req["request"]["original_utterance"].lower() in ["2", "вторая", "два"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона дракону, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"]["text"] = f"Вы попали топором дракону в голову, чтобы получить награду, скажите 'получить награду'"
                            res["response"]["tts"] = f'<speaker audio="alice-sounds-game-win-3.opus">Вы попали топором дракону ' \
                                                     f'в голову, чтобы получить награду, скажите "получить награду"'
                            state.fights = 1
                            state.fight_step = 1
                            state.etap = 'ending'
                    elif req["request"]["original_utterance"].lower() in ["3", "третья", "три"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"]["text"] = f"Вы раскрошили голову дракону моргенштерном, чтобы получить награду, скажите 'получить награду'"
                            res["response"]["tts"] = f'<speaker audio="alice-sounds-game-win-3.opus"> Вы раскрошили голову дракону' \
                                                     f' моргенштерном, чтобы получить награду, скажите "получить награду"'
                            state.fights = 1
                            state.fight_step = 1
                            state.etap = 'ending'
                    else:
                        res["response"]["text"] = f"скажите, какую атаку вы хотите использовать один два или три, \n" \
                                                  f"чтобы посмотреть атаки, скажите 'способности варвара'"

                elif state.fight_step == -1:
                    if req["request"]["original_utterance"].lower() in ["продолжить", "дальше"]:
                        enem_atc = random.randint(state.stateen["enemmaxa"], state.stateen["enemmina"])
                        enem_atsh = random.randint(15, 20)
                        if enem_atsh >= state.state["shield"] and (state.state["hp"] + enem_atc) > 0:
                            res["response"][
                                "text"] = f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                          f"урона, теперь кидайте кубик щита" \
                                          f" напоминаю, чтобы пробить щит скажите 'пробить щит'"
                            state.state["hp"] = state.state["hp"] + enem_atc
                            state.fight_step = 2
                        elif enem_atsh >= state.state["shield"] and (state.state["hp"] + enem_atc) <= 0:
                            res["response"][
                                "text"] = f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                          f"урона, и к сожалению вы погибли..." \
                                          f" захотите поиграть еще, я всегда тут"
                            res["response"]["tts"] = f'<speaker audio="alice-sounds-game-loss-3.opus">'\
                                                      f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                                      f"урона, и к сожалению вы погибли..." \
                                                      f" захотите поиграть еще, я всегда тут"
                            res['response']['end_session'] = True
                            state.state = {}
                            state.etap = "askname"
                            state.fights = 0
                            state.fight_step = 1
                            state.num = [1, 3, 4, 6, 7, 8, 9, 10, 11, 13]

                        else:
                            res["response"][
                                "text"] = f"Враг выбросил {enem_atsh} и не пробил ваш щит теперь вы кидаете кубик щита" \
                                          f" напоминаю, чтобы пробить щит скажите 'пробить щит'"
                            state.fight_step = 2
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить'"

            elif state.fights == 2:
                n = random.choice(state.num)
                barbarian2 = db_sess.query(Barbarian).filter(Barbarian.id == n).first()
                if state.fight_step == 1:
                    state.stateen["enem_hp"] = barbarian2.enemyhp
                    state.stateen["enem"] = barbarian2.enemy
                    state.stateen["enemshi"] = barbarian2.shield
                    state.stateen["enemmina"] = barbarian2.minatack
                    state.stateen["enemmaxa"] = barbarian2.maxatack
                    state.stateen["enemfirst"] = barbarian2.firstkill
                    state.stateen["enemsecond"] = barbarian2.secondkill
                    state.stateen["enemthird"] = barbarian2.thirdkill
                    if req["request"]["original_utterance"].lower() in ["продолжить приключение",
                                                                        "продолжи приключение"]:
                        res["response"]["text"] = f"Вы наткнулись на {state.stateen['enem']}\n" \
                                                  f"Параметры врага:\n" \
                                                  f"хп: {state.stateen['enem_hp']}\n" \
                                                  f"щит: {state.stateen['enemshi']}\n" \
                                                  f"минимальная атака: {state.stateen['enemmina']}\n" \
                                                  f"максимальная атака: {state.stateen['enemmaxa']}\n" \
                                                  f"Чтобы ударить врага пробейте его щит, скажите 'пробить щит'"
                        state.fight_step = 2

                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить приключение'"
                elif state.fight_step == 2:
                    if req["request"]["original_utterance"].lower() in ["пробей щит", "пробить щит"]:
                        state.shi = random.randint(15, 20)
                        res["response"][
                            "text"] = f"Вы выбросили {state.shi}, чтобы узнать пробили ли вы щит скажите 'продолжить'"
                        state.fight_step = 3
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы пробить щит скажите 'пробить щит'"
                elif state.fight_step == 3:
                    if req["request"]["original_utterance"].lower() in ["продолжить", "дальше"]:
                        if state.shi >= state.stateen["enemshi"]:
                            res["response"]["text"] = "Вы пробили щит, теперь бросьте кубик урона, чтобы это сделать " \
                                                      "скажите 'нанести урон'"
                            state.fight_step = 4
                        else:
                            res["response"][
                                "text"] = "Вы не пробили щит, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить'"
                elif state.fight_step == 4:
                    if req["request"]["original_utterance"].lower() in ["нанеси урон", "нанести урон"]:
                        state.atc = random.randint(state.state["mina"], state.state["maxa"])
                        state.stateen["enem_hp"] = state.stateen["enem_hp"] - state.atc
                        res["response"][
                            "text"] = f"теперь скажите, какую атаку вы хотите использовать один два или три, \n" \
                                      f"чтобы посмотреть атаки, скажите 'способности варвара'"
                        state.fight_step = 5
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы нанести урон скажите 'нанести урон'"
                elif state.fight_step == 5:
                    if req["request"]["original_utterance"].lower() in ["1", "первая", "один"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"][
                                "text"] = f"{state.stateen['enemfirst']}. Вы узнали, что в вашем королевстве беда! Казну обокрал " \
                                          f"дракон, чтобы найти логово дракона, скажите 'найти дракона'"
                            state.fights = 3
                            state.fight_step = 1
                            state.num.remove(n)
                    elif req["request"]["original_utterance"].lower() in ["2", "вторая", "два"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"][
                                "text"] = f"{state.stateen['enemsecond']}. Вы узнали, что в вашем королевстве беда! Казну обокрал " \
                                          f"дракон, чтобы найти логово дракона, скажите 'найти дракона'"
                            state.fights = 3
                            state.fight_step = 1
                            state.num.remove(n)
                    elif req["request"]["original_utterance"].lower() in ["3", "третья", "три"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"][
                                "text"] = f"{state.stateen['enemthird']}. Вы узнали, что в вашем королевстве беда! Казну обокрал " \
                                          f"дракон, чтобы найти логово дракона, скажите 'найти дракона'"
                            state.fights = 3
                            state.fight_step = 1
                            state.num.remove(n)
                    else:
                        res["response"]["text"] = f"скажите, какую атаку вы хотите использовать один два или три, \n" \
                                                  f"чтобы посмотреть атаки, скажите 'способности варвара'"

                elif state.fight_step == -1:
                    if req["request"]["original_utterance"].lower() in ["продолжить", "дальше"]:
                        enem_atc = random.randint(state.stateen["enemmaxa"], state.stateen["enemmina"])
                        enem_atsh = random.randint(15, 20)
                        if enem_atsh >= state.state["shield"] and (state.state["hp"] + enem_atc) > 0:
                            res["response"][
                                "text"] = f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                          f"урона, теперь кидайте кубик щита" \
                                          f" напоминаю, чтобы пробить щит скажите 'пробить щит'"
                            state.state["hp"] = state.state["hp"] + enem_atc
                            state.fight_step = 2
                        elif enem_atsh >= state.state["shield"] and (state.state["hp"] + enem_atc) <= 0:
                            res["response"][
                                "text"] = f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                          f"урона, и к сожалению вы погибли..." \
                                          f" захотите поиграть еще, я всегда тут"
                            res["response"]["tts"] = f'<speaker audio="alice-sounds-game-loss-3.opus">'\
                                                      f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                                      f"урона, и к сожалению вы погибли..." \
                                                      f" захотите поиграть еще, я всегда тут"
                            res['response']['end_session'] = True
                            state.state = {}
                            state.etap = "askname"
                            state.fights = 0
                            state.fight_step = 1
                            state.num = [1, 3, 4, 6, 7, 8, 9, 10, 11, 13]

                        else:
                            res["response"][
                                "text"] = f"Враг выбросил {enem_atsh} и не пробил ваш щит теперь вы кидаете кубик щита" \
                                          f" напоминаю, чтобы пробить щит скажите 'пробить щит'"
                            state.fight_step = 2
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить'"

            elif state.fights == 1:
                n = random.choice(state.num)
                barbarian1 = db_sess.query(Barbarian).filter(Barbarian.id == n).first()
                if state.fight_step == 1:
                    state.stateen["enem_hp"] = barbarian1.enemyhp
                    state.stateen["enem"] = barbarian1.enemy
                    state.stateen["enemshi"] = barbarian1.shield
                    state.stateen["enemmina"] = barbarian1.minatack
                    state.stateen["enemmaxa"] = barbarian1.maxatack
                    state.stateen["enemfirst"] = barbarian1.firstkill
                    state.stateen["enemsecond"] = barbarian1.secondkill
                    state.stateen["enemthird"] = barbarian1.thirdkill
                    if req["request"]["original_utterance"].lower() in ["продолжить приключение",
                                                                        "продолжи приключение"]:
                        res["response"]["text"] = f"Вы наткнулись на {state.stateen['enem']}\n" \
                                                  f"Параметры врага:\n" \
                                                  f"хп: {state.stateen['enem_hp']}\n" \
                                                  f"щит: {state.stateen['enemshi']}\n" \
                                                  f"минимальная атака: {state.stateen['enemmina']}\n" \
                                                  f"максимальная атака: {state.stateen['enemmaxa']}\n" \
                                                  f"Чтобы ударить врага пробейте его щит, скажите 'пробить щит'"
                        state.fight_step = 2

                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить приключение'"
                elif state.fight_step == 2:
                    if req["request"]["original_utterance"].lower() in ["пробей щит", "пробить щит"]:
                        state.shi = random.randint(15, 20)
                        res["response"][
                            "text"] = f"Вы выбросили {state.shi}, чтобы узнать пробили ли вы щит скажите 'продолжить'"
                        state.fight_step = 3
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы пробить щит скажите 'пробить щит'"
                elif state.fight_step == 3:
                    if req["request"]["original_utterance"].lower() in ["продолжить", "дальше"]:
                        if state.shi >= state.stateen["enemshi"]:
                            res["response"]["text"] = "Вы пробили щит, теперь бросьте кубик урона, чтобы это сделать " \
                                                      "скажите 'нанести урон'"
                            state.fight_step = 4
                        else:
                            res["response"][
                                "text"] = "Вы не пробили щит, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить'"
                elif state.fight_step == 4:
                    if req["request"]["original_utterance"].lower() in ["нанеси урон", "нанести урон"]:
                        state.atc = random.randint(state.state["mina"], state.state["maxa"])
                        state.stateen["enem_hp"] = state.stateen["enem_hp"] - state.atc
                        res["response"][
                            "text"] = f"теперь скажите, какую атаку вы хотите использовать один два или три, \n" \
                                      f"чтобы посмотреть атаки, скажите 'способности варвара'"
                        state.fight_step = 5
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы нанести урон скажите 'нанести урон'"
                elif state.fight_step == 5:
                    if req["request"]["original_utterance"].lower() in ["1", "первая", "один"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"][
                                "text"] = f"{state.stateen['enemfirst']}, чтобы продолжить, скажите 'продолжить приключение'"
                            state.fights = 2
                            state.fight_step = 1
                            state.num.remove(n)
                    elif req["request"]["original_utterance"].lower() in ["2", "вторая", "два"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"][
                                "text"] = f"{state.stateen['enemsecond']}, чтобы продолжить, скажите 'продолжить приключение'"
                            state.fights = 2
                            state.fight_step = 1
                            state.num.remove(n)
                    elif req["request"]["original_utterance"].lower() in ["3", "третья", "три"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"][
                                "text"] = f"{state.stateen['enemthird']}, чтобы продолжить, скажите 'продолжить приключение'"
                            state.fights = 2
                            state.fight_step = 1
                            state.num.remove(n)
                    else:
                        res["response"]["text"] = f"скажите, какую атаку вы хотите использовать один два или три, \n" \
                                                  f"чтобы посмотреть атаки, скажите 'способности варвара'"

                elif state.fight_step == -1:
                    if req["request"]["original_utterance"].lower() in ["продолжить", "дальше"]:
                        enem_atc = random.randint(state.stateen["enemmaxa"], state.stateen["enemmina"])
                        enem_atsh = random.randint(15, 20)
                        if enem_atsh >= state.state["shield"] and (state.state["hp"] + enem_atc) > 0:
                            res["response"][
                                "text"] = f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                          f"урона, теперь кидайте кубик щита" \
                                          f" напоминаю, чтобы пробить щит скажите 'пробить щит'"
                            state.state["hp"] = state.state["hp"] + enem_atc
                            state.fight_step = 2
                        elif enem_atsh >= state.state["shield"] and (state.state["hp"] + enem_atc) <= 0:
                            res["response"][
                                "text"] = f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                          f"урона, и к сожалению вы погибли..." \
                                          f" захотите поиграть еще, я всегда тут"
                            res["response"]["tts"] = f'<speaker audio="alice-sounds-game-loss-3.opus">'\
                                                      f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                                      f"урона, и к сожалению вы погибли..." \
                                                      f" захотите поиграть еще, я всегда тут"
                            res['response']['end_session'] = True
                            state.state = {}
                            state.etap = "askname"
                            state.fights = 0
                            state.fight_step = 1
                            state.num = [1, 3, 4, 6, 7, 8, 9, 10, 11, 13]

                        else:
                            res["response"][
                                "text"] = f"Враг выбросил {enem_atsh} и не пробил ваш щит теперь вы кидаете кубик щита" \
                                          f" напоминаю, чтобы пробить щит скажите 'пробить щит'"
                            state.fight_step = 2
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить'"

            elif state.fights == 0:
                n = random.choice(state.num)
                barbarian0 = db_sess.query(Barbarian).filter(Barbarian.id == n).first()
                if state.fight_step == 1:
                    state.stateen["enem_hp"] = barbarian0.enemyhp
                    state.stateen["enem"] = barbarian0.enemy
                    state.stateen["enemshi"] = barbarian0.shield
                    state.stateen["enemmina"] = barbarian0.minatack
                    state.stateen["enemmaxa"] = barbarian0.maxatack
                    state.stateen["enemfirst"] = barbarian0.firstkill
                    state.stateen["enemsecond"] = barbarian0.secondkill
                    state.stateen["enemthird"] = barbarian0.thirdkill
                    if req["request"]["original_utterance"].lower() in ["начать приключение", "начни приключение"]:
                        res["response"]["text"] = f"Вы наткнулись на {state.stateen['enem']}\n" \
                                                  f"Параметры врага:\n" \
                                                  f"хп: {state.stateen['enem_hp']}\n" \
                                                  f"щит: {state.stateen['enemshi']}\n" \
                                                  f"минимальная атака: {state.stateen['enemmina']}\n" \
                                                  f"максимальная атака: {state.stateen['enemmaxa']}\n" \
                                                  f"Чтобы ударить врага пробейте его щит, скажите 'пробить щит'"
                        state.fight_step = 2

                    else:
                        res["response"]["text"] = "Напоминаю, чтобы начать скажите 'начать приключение'"
                elif state.fight_step == 2:
                    if req["request"]["original_utterance"].lower() in ["пробей щит", "пробить щит"]:
                        state.shi = random.randint(15, 20)
                        res["response"][
                            "text"] = f"Вы выбросили {state.shi}, чтобы узнать пробили ли вы щит скажите 'продолжить'"
                        state.fight_step = 3
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы пробить щит скажите 'пробить щит'"
                elif state.fight_step == 3:
                    if req["request"]["original_utterance"].lower() in ["продолжить", "дальше"]:
                        if state.shi >= state.stateen["enemshi"]:
                            res["response"]["text"] = "Вы пробили щит, теперь бросьте кубик урона, чтобы это сделать " \
                                                      "скажите 'нанести урон'"
                            state.fight_step = 4
                        else:
                            res["response"][
                                "text"] = "Вы не пробили щит, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить'"
                elif state.fight_step == 4:
                    if req["request"]["original_utterance"].lower() in ["нанеси урон", "нанести урон"]:
                        state.atc = random.randint(state.state["mina"], state.state["maxa"])
                        state.stateen["enem_hp"] = state.stateen["enem_hp"] - state.atc
                        res["response"][
                            "text"] = f"теперь скажите, какую атаку вы хотите использовать один два или три, \n" \
                                      f"чтобы посмотреть атаки, скажите 'способности варвара'"
                        state.fight_step = 5
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы нанести урон скажите 'нанести урон'"
                elif state.fight_step == 5:
                    if req["request"]["original_utterance"].lower() in ["1", "первая", "один"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"][
                                "text"] = f"{state.stateen['enemfirst']}, чтобы продолжить, скажите 'продолжить приключение'"
                            state.fights = 1
                            state.fight_step = 1
                            state.num.remove(n)
                    elif req["request"]["original_utterance"].lower() in ["2", "вторая", "два"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"][
                                "text"] = f"{state.stateen['enemsecond']}, чтобы продолжить, скажите 'продолжить приключение'"
                            state.fights = 1
                            state.fight_step = 1
                            state.num.remove(n)
                    elif req["request"]["original_utterance"].lower() in ["3", "третья", "три"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"][
                                "text"] = f"{state.stateen['enemthird']}, чтобы продолжить, скажите 'продолжить приключение'"
                            state.fights = 1
                            state.fight_step = 1
                            state.num.remove(n)
                    else:
                        res["response"]["text"] = f"скажите, какую атаку вы хотите использовать один два или три, \n" \
                                                  f"чтобы посмотреть атаки, скажите 'способности врвара'"

                elif state.fight_step == -1:
                    if req["request"]["original_utterance"].lower() in ["продолжить", "дальше"]:
                        enem_atc = random.randint(state.stateen["enemmaxa"], state.stateen["enemmina"])
                        enem_atsh = random.randint(15, 20)
                        if enem_atsh >= state.state["shield"] and (state.state["hp"] + enem_atc) > 0:
                            res["response"][
                                "text"] = f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                          f"урона, теперь кидайте кубик щита" \
                                          f" напоминаю, чтобы пробить щит скажите 'пробить щит'"
                            state.state["hp"] = state.state["hp"] + enem_atc
                            state.fight_step = 2
                        elif enem_atsh >= state.state["shield"] and (state.state["hp"] + enem_atc) <= 0:
                            res["response"][
                                "text"] = f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                          f"урона, и к сожалению вы погибли..." \
                                          f" захотите поиграть еще, я всегда тут"
                            res["response"]["tts"] = f'<speaker audio="alice-sounds-game-loss-3.opus">'\
                                                      f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                                      f"урона, и к сожалению вы погибли..." \
                                                      f" захотите поиграть еще, я всегда тут"
                            res['response']['end_session'] = True
                            state.state = {}
                            state.etap = "askname"
                            state.fights = 0
                            state.fight_step = 1
                            state.num = [1, 3, 4, 6, 7, 8, 9, 10, 11, 13]

                        else:
                            res["response"][
                                "text"] = f"Враг выбросил {enem_atsh} и не пробил ваш щит теперь вы кидаете кубик щита" \
                                          f" напоминаю, чтобы пробить щит скажите 'пробить щит'"
                            state.fight_step = 2
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить'"

        elif state.state["role"] == "рыцарь":
            if state.fights == 3:
                n = 12
                knight3 = db_sess.query(Knight).filter(Knight.id == n).first()
                if state.fight_step == 1:
                    state.stateen["enem_hp"] = knight3.enemyhp
                    state.stateen["enem"] = knight3.enemy
                    state.stateen["enemshi"] = knight3.shield
                    state.stateen["enemmina"] = knight3.minatack
                    state.stateen["enemmaxa"] = knight3.maxatack
                    state.stateen["enemfirst"] = knight3.firstkill
                    state.stateen["enemsecond"] = knight3.secondkill
                    state.stateen["enemthird"] = knight3.thirdkill
                    if req["request"]["original_utterance"].lower() in ["найти дракона", "искать дракона"]:
                        res["response"]["text"] = f"Вы встретили огромного дракона, сторожащего золото\n" \
                                                  f"Параметры дракона:\n" \
                                                  f"хп: {state.stateen['enem_hp']}\n" \
                                                  f"щит: {state.stateen['enemshi']}\n" \
                                                  f"минимальная атака: {state.stateen['enemmina']}\n" \
                                                  f"максимальная атака: {state.stateen['enemmaxa']}\n" \
                                                  f"Чтобы ударить дракона пробейте его щит, скажите 'пробить щит'"
                        state.fight_step = 2

                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить приключение'"
                elif state.fight_step == 2:
                    if req["request"]["original_utterance"].lower() in ["пробей щит", "пробить щит"]:
                        state.shi = random.randint(15, 20)
                        res["response"][
                            "text"] = f"Вы выбросили {state.shi}, чтобы узнать пробили ли вы щит скажите 'продолжить'"
                        state.fight_step = 3
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы пробить щит скажите 'пробить щит'"
                elif state.fight_step == 3:
                    if req["request"]["original_utterance"].lower() in ["продолжить", "дальше"]:
                        if state.shi >= state.stateen["enemshi"]:
                            res["response"]["text"] = "Вы пробили щит, теперь бросьте кубик урона, чтобы это сделать " \
                                                      "скажите 'нанести урон'"
                            state.fight_step = 4
                        else:
                            res["response"][
                                "text"] = "Вы не пробили щит, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить'"
                elif state.fight_step == 4:
                    if req["request"]["original_utterance"].lower() in ["нанеси урон", "нанести урон"]:
                        state.atc = random.randint(state.state["mina"], state.state["maxa"])
                        state.stateen["enem_hp"] = state.stateen["enem_hp"] - state.atc
                        res["response"][
                            "text"] = f"теперь скажите, какую атаку вы хотите использовать один два или три, \n" \
                                      f"чтобы посмотреть атаки, скажите 'способности рыцаря'"
                        state.fight_step = 5
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы нанести урон скажите 'нанести урон'"
                elif state.fight_step == 5:
                    if req["request"]["original_utterance"].lower() in ["1", "первая", "один"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"]["text"] = f"Вы отрубили голову дракону, чтобы получить награду, скажите 'получить награду'"
                            res["response"]["tts"] = f'<speaker audio="alice-sounds-game-win-3.opus"> Вы отрубили голову дракону, ' \
                                                     f'чтобы получить награду, скажите "получить награду"'
                            state.fights = 1
                            state.fight_step = 1
                            state.etap = 'ending'
                    elif req["request"]["original_utterance"].lower() in ["2", "вторая", "два"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона дракону, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"]["text"] = f"Вы задушили дракона, придавив его шею щитом, чтобы получить награду, скажите 'получить награду'"
                            res["response"]["tts"] = f'<speaker audio="alice-sounds-game-win-3.opus"> Вы задушили дракона, ' \
                                                     f'придавив его шею щитом, чтобы получить награду, скажите "получить награду"'
                            state.fights = 1
                            state.fight_step = 1
                            state.etap = 'ending'
                    elif req["request"]["original_utterance"].lower() in ["3", "третья", "три"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"]["text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"]["text"] = f"Вы проткнули дракона копьем, чтобы получить награду, скажите 'получить награду'"
                            res["response"]["tts"] = f'<speaker audio="alice-sounds-game-win-3.opus"> Вы проткнули дракона копьем,' \
                                                     f' чтобы получить награду, скажите "получить награду"'
                            state.fights = 1
                            state.fight_step = 1
                            state.etap = 'ending'
                    else:
                        res["response"]["text"] = f"скажите, какую атаку вы хотите использовать один два или три, \n" \
                                                  f"чтобы посмотреть атаки, скажите 'способности рыцаря'"

                elif state.fight_step == -1:
                    if req["request"]["original_utterance"].lower() in ["продолжить", "дальше"]:
                        enem_atc = random.randint(state.stateen["enemmaxa"], state.stateen["enemmina"])
                        enem_atsh = random.randint(15, 20)
                        if enem_atsh >= state.state["shield"] and (state.state["hp"] + enem_atc) > 0:
                            res["response"][
                                "text"] = f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                          f"урона, теперь кидайте кубик щита" \
                                          f" напоминаю, чтобы пробить щит скажите 'пробить щит'"
                            state.state["hp"] = state.state["hp"] + enem_atc
                            state.fight_step = 2
                        elif enem_atsh >= state.state["shield"] and (state.state["hp"] + enem_atc) <= 0:
                            res["response"][
                                "text"] = f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                          f"урона, и к сожалению вы погибли..." \
                                          f" захотите поиграть еще, я всегда тут"
                            res["response"]["tts"] = f'<speaker audio="alice-sounds-game-loss-3.opus">'\
                                                      f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                                      f"урона, и к сожалению вы погибли..." \
                                                      f" захотите поиграть еще, я всегда тут"
                            res['response']['end_session'] = True
                            state.state = {}
                            state.etap = "askname"
                            state.fights = 0
                            state.fight_step = 1
                            state.num = [1, 3, 4, 6, 7, 8, 9, 10, 11, 13]

                        else:
                            res["response"][
                                "text"] = f"Враг выбросил {enem_atsh} и не пробил ваш щит теперь вы кидаете кубик щита" \
                                          f" напоминаю, чтобы пробить щит скажите 'пробить щит'"
                            state.fight_step = 2
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить'"

            elif state.fights == 2:
                n = random.choice(state.num)
                knight2 = db_sess.query(Knight).filter(Knight.id == n).first()
                if state.fight_step == 1:
                    state.stateen["enem_hp"] = knight2.enemyhp
                    state.stateen["enem"] = knight2.enemy
                    state.stateen["enemshi"] = knight2.shield
                    state.stateen["enemmina"] = knight2.minatack
                    state.stateen["enemmaxa"] = knight2.maxatack
                    state.stateen["enemfirst"] = knight2.firstkill
                    state.stateen["enemsecond"] = knight2.secondkill
                    state.stateen["enemthird"] = knight2.thirdkill
                    if req["request"]["original_utterance"].lower() in ["продолжить приключение",
                                                                        "продолжи приключение"]:
                        res["response"]["text"] = f"Вы наткнулись на {state.stateen['enem']}\n" \
                                                  f"Параметры врага:\n" \
                                                  f"хп: {state.stateen['enem_hp']}\n" \
                                                  f"щит: {state.stateen['enemshi']}\n" \
                                                  f"минимальная атака: {state.stateen['enemmina']}\n" \
                                                  f"максимальная атака: {state.stateen['enemmaxa']}\n" \
                                                  f"Чтобы ударить врага пробейте его щит, скажите 'пробить щит'"
                        state.fight_step = 2

                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить приключение'"
                elif state.fight_step == 2:
                    if req["request"]["original_utterance"].lower() in ["пробей щит", "пробить щит"]:
                        state.shi = random.randint(15, 20)
                        res["response"][
                            "text"] = f"Вы выбросили {state.shi}, чтобы узнать пробили ли вы щит скажите 'продолжить'"
                        state.fight_step = 3
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы пробить щит скажите 'пробить щит'"
                elif state.fight_step == 3:
                    if req["request"]["original_utterance"].lower() in ["продолжить", "дальше"]:
                        if state.shi >= state.stateen["enemshi"]:
                            res["response"]["text"] = "Вы пробили щит, теперь бросьте кубик урона, чтобы это сделать " \
                                                      "скажите 'нанести урон'"
                            state.fight_step = 4
                        else:
                            res["response"][
                                "text"] = "Вы не пробили щит, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить'"
                elif state.fight_step == 4:
                    if req["request"]["original_utterance"].lower() in ["нанеси урон", "нанести урон"]:
                        state.atc = random.randint(state.state["mina"], state.state["maxa"])
                        state.stateen["enem_hp"] = state.stateen["enem_hp"] - state.atc
                        res["response"][
                            "text"] = f"теперь скажите, какую атаку вы хотите использовать один два или три, \n" \
                                      f"чтобы посмотреть атаки, скажите 'способности рыцаря'"
                        state.fight_step = 5
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы нанести урон скажите 'нанести урон'"
                elif state.fight_step == 5:
                    if req["request"]["original_utterance"].lower() in ["1", "первая", "один"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"][
                                "text"] = f"{state.stateen['enemfirst']}. Вы узнали, что в вашем королевстве беда! Казну обокрал " \
                                          f"дракон, чтобы найти логово дракона, скажите 'найти дракона'"
                            state.fights = 3
                            state.fight_step = 1
                            state.num.remove(n)
                    elif req["request"]["original_utterance"].lower() in ["2", "вторая", "два"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"][
                                "text"] = f"{state.stateen['enemsecond']}. Вы узнали, что в вашем королевстве беда! Казну обокрал " \
                                          f"дракон, чтобы найти логово дракона, скажите 'найти дракона'"
                            state.fights = 3
                            state.fight_step = 1
                            state.num.remove(n)
                    elif req["request"]["original_utterance"].lower() in ["3", "третья", "три"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"][
                                "text"] = f"{state.stateen['enemthird']}. Вы узнали, что в вашем королевстве беда! Казну обокрал " \
                                          f"дракон, чтобы найти логово дракона, скажите 'найти дракона'"
                            state.fights = 3
                            state.fight_step = 1
                            state.num.remove(n)
                    else:
                        res["response"]["text"] = f"скажите, какую атаку вы хотите использовать один два или три, \n" \
                                                  f"чтобы посмотреть атаки, скажите 'способности рыцаря'"

                elif state.fight_step == -1:
                    if req["request"]["original_utterance"].lower() in ["продолжить", "дальше"]:
                        enem_atc = random.randint(state.stateen["enemmaxa"], state.stateen["enemmina"])
                        enem_atsh = random.randint(15, 20)
                        if enem_atsh >= state.state["shield"] and (state.state["hp"] + enem_atc) > 0:
                            res["response"][
                                "text"] = f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                          f"урона, теперь кидайте кубик щита" \
                                          f" напоминаю, чтобы пробить щит скажите 'пробить щит'"
                            state.state["hp"] = state.state["hp"] + enem_atc
                            state.fight_step = 2
                        elif enem_atsh >= state.state["shield"] and (state.state["hp"] + enem_atc) <= 0:
                            res["response"][
                                "text"] = f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                          f"урона, и к сожалению вы погибли..." \
                                          f" захотите поиграть еще, я всегда тут"
                            res["response"]["tts"] = f'<speaker audio="alice-sounds-game-loss-3.opus">'\
                                                      f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                                      f"урона, и к сожалению вы погибли..." \
                                                      f" захотите поиграть еще, я всегда тут"
                            res['response']['end_session'] = True
                            state.state = {}
                            state.etap = "askname"
                            state.fights = 0
                            state.fight_step = 1
                            state.num = [1, 3, 4, 6, 7, 8, 9, 10, 11, 13]

                        else:
                            res["response"][
                                "text"] = f"Враг выбросил {enem_atsh} и не пробил ваш щит теперь вы кидаете кубик щита" \
                                          f" напоминаю, чтобы пробить щит скажите 'пробить щит'"
                            state.fight_step = 2
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить'"

            elif state.fights == 1:
                n = random.choice(state.num)
                knight1 = db_sess.query(Knight).filter(Knight.id == n).first()
                if state.fight_step == 1:
                    state.stateen["enem_hp"] = knight1.enemyhp
                    state.stateen["enem"] = knight1.enemy
                    state.stateen["enemshi"] = knight1.shield
                    state.stateen["enemmina"] = knight1.minatack
                    state.stateen["enemmaxa"] = knight1.maxatack
                    state.stateen["enemfirst"] = knight1.firstkill
                    state.stateen["enemsecond"] = knight1.secondkill
                    state.stateen["enemthird"] = knight1.thirdkill
                    if req["request"]["original_utterance"].lower() in ["продолжить приключение",
                                                                        "продолжи приключение"]:
                        res["response"]["text"] = f"Вы наткнулись на {state.stateen['enem']}\n" \
                                                  f"Параметры врага:\n" \
                                                  f"хп: {state.stateen['enem_hp']}\n" \
                                                  f"щит: {state.stateen['enemshi']}\n" \
                                                  f"минимальная атака: {state.stateen['enemmina']}\n" \
                                                  f"максимальная атака: {state.stateen['enemmaxa']}\n" \
                                                  f"Чтобы ударить врага пробейте его щит, скажите 'пробить щит'"
                        state.fight_step = 2

                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить приключение'"
                elif state.fight_step == 2:
                    if req["request"]["original_utterance"].lower() in ["пробей щит", "пробить щит"]:
                        state.shi = random.randint(15, 20)
                        res["response"][
                            "text"] = f"Вы выбросили {state.shi}, чтобы узнать пробили ли вы щит скажите 'продолжить'"
                        state.fight_step = 3
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы пробить щит скажите 'пробить щит'"
                elif state.fight_step == 3:
                    if req["request"]["original_utterance"].lower() in ["продолжить", "дальше"]:
                        if state.shi >= state.stateen["enemshi"]:
                            res["response"]["text"] = "Вы пробили щит, теперь бросьте кубик урона, чтобы это сделать " \
                                                      "скажите 'нанести урон'"
                            state.fight_step = 4
                        else:
                            res["response"][
                                "text"] = "Вы не пробили щит, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить'"
                elif state.fight_step == 4:
                    if req["request"]["original_utterance"].lower() in ["нанеси урон", "нанести урон"]:
                        state.atc = random.randint(state.state["mina"], state.state["maxa"])
                        state.stateen["enem_hp"] = state.stateen["enem_hp"] - state.atc
                        res["response"][
                            "text"] = f"теперь скажите, какую атаку вы хотите использовать один два или три, \n" \
                                      f"чтобы посмотреть атаки, скажите 'способности рыцаря'"
                        state.fight_step = 5
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы нанести урон скажите 'нанести урон'"
                elif state.fight_step == 5:
                    if req["request"]["original_utterance"].lower() in ["1", "первая", "один"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"][
                                "text"] = f"{state.stateen['enemfirst']}, чтобы продолжить, скажите 'продолжить приключение'"
                            state.fights = 2
                            state.fight_step = 1
                            state.num.remove(n)
                    elif req["request"]["original_utterance"].lower() in ["2", "вторая", "два"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"][
                                "text"] = f"{state.stateen['enemsecond']}, чтобы продолжить, скажите 'продолжить приключение'"
                            state.fights = 2
                            state.fight_step = 1
                            state.num.remove(n)
                    elif req["request"]["original_utterance"].lower() in ["3", "третья", "три"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"][
                                "text"] = f"{state.stateen['enemthird']}, чтобы продолжить, скажите 'продолжить приключение'"
                            state.fights = 2
                            state.fight_step = 1
                            state.num.remove(n)
                    else:
                        res["response"]["text"] = f"скажите, какую атаку вы хотите использовать один два или три, \n" \
                                                  f"чтобы посмотреть атаки, скажите 'способности рыцаря'"

                elif state.fight_step == -1:
                    if req["request"]["original_utterance"].lower() in ["продолжить", "дальше"]:
                        enem_atc = random.randint(state.stateen["enemmaxa"], state.stateen["enemmina"])
                        enem_atsh = random.randint(15, 20)
                        if enem_atsh >= state.state["shield"] and (state.state["hp"] + enem_atc) > 0:
                            res["response"][
                                "text"] = f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                          f"урона, теперь кидайте кубик щита" \
                                          f" напоминаю, чтобы пробить щит скажите 'пробить щит'"
                            state.state["hp"] = state.state["hp"] + enem_atc
                            state.fight_step = 2
                        elif enem_atsh >= state.state["shield"] and (state.state["hp"] + enem_atc) <= 0:
                            res["response"][
                                "text"] = f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                          f"урона, и к сожалению вы погибли..." \
                                          f" захотите поиграть еще, я всегда тут"
                            res["response"]["tts"] = f'<speaker audio="alice-sounds-game-loss-3.opus">'\
                                                      f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                                      f"урона, и к сожалению вы погибли..." \
                                                      f" захотите поиграть еще, я всегда тут"
                            res['response']['end_session'] = True
                            state.state = {}
                            state.etap = "askname"
                            state.fights = 0
                            state.fight_step = 1
                            state.num = [1, 3, 4, 6, 7, 8, 9, 10, 11, 13]

                        else:
                            res["response"][
                                "text"] = f"Враг выбросил {enem_atsh} и не пробил ваш щит теперь вы кидаете кубик щита" \
                                          f" напоминаю, чтобы пробить щит скажите 'пробить щит'"
                            state.fight_step = 2
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить'"

            elif state.fights == 0:
                n = random.choice(state.num)
                knight0 = db_sess.query(Knight).filter(Knight.id == n).first()
                if state.fight_step == 1:
                    state.stateen["enem_hp"] = knight0.enemyhp
                    state.stateen["enem"] = knight0.enemy
                    state.stateen["enemshi"] = knight0.shield
                    state.stateen["enemmina"] = knight0.minatack
                    state.stateen["enemmaxa"] = knight0.maxatack
                    state.stateen["enemfirst"] = knight0.firstkill
                    state.stateen["enemsecond"] = knight0.secondkill
                    state.stateen["enemthird"] = knight0.thirdkill
                    if req["request"]["original_utterance"].lower() in ["начать приключение", "начни приключение"]:
                        res["response"]["text"] = f"Вы наткнулись на {state.stateen['enem']}\n" \
                                                  f"Параметры врага:\n" \
                                                  f"хп: {state.stateen['enem_hp']}\n" \
                                                  f"щит: {state.stateen['enemshi']}\n" \
                                                  f"минимальная атака: {state.stateen['enemmina']}\n" \
                                                  f"максимальная атака: {state.stateen['enemmaxa']}\n" \
                                                  f"Чтобы ударить врага пробейте его щит, скажите 'пробить щит'"
                        state.fight_step = 2

                    else:
                        res["response"]["text"] = "Напоминаю, чтобы начать скажите 'начать приключение'"
                elif state.fight_step == 2:
                    if req["request"]["original_utterance"].lower() in ["пробей щит", "пробить щит"]:
                        state.shi = random.randint(15, 20)
                        res["response"][
                            "text"] = f"Вы выбросили {state.shi}, чтобы узнать пробили ли вы щит скажите 'продолжить'"
                        state.fight_step = 3
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы пробить щит скажите 'пробить щит'"
                elif state.fight_step == 3:
                    if req["request"]["original_utterance"].lower() in ["продолжить", "дальше"]:
                        if state.shi >= state.stateen["enemshi"]:
                            res["response"]["text"] = "Вы пробили щит, теперь бросьте кубик урона, чтобы это сделать " \
                                                      "скажите 'нанести урон'"
                            state.fight_step = 4
                        else:
                            res["response"][
                                "text"] = "Вы не пробили щит, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить'"
                elif state.fight_step == 4:
                    if req["request"]["original_utterance"].lower() in ["нанеси урон", "нанести урон"]:
                        state.atc = random.randint(state.state["mina"], state.state["maxa"])
                        state.stateen["enem_hp"] = state.stateen["enem_hp"] - state.atc
                        res["response"][
                            "text"] = f"теперь скажите, какую атаку вы хотите использовать один два или три, \n" \
                                      f"чтобы посмотреть атаки, скажите 'способности рыцаря'"
                        state.fight_step = 5
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы нанести урон скажите 'нанести урон'"
                elif state.fight_step == 5:
                    if req["request"]["original_utterance"].lower() in ["1", "первая", "один"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"][
                                "text"] = f"{state.stateen['enemfirst']}, чтобы продолжить, скажите 'продолжить приключение'"
                            state.fights = 1
                            state.fight_step = 1
                            state.num.remove(n)
                    elif req["request"]["original_utterance"].lower() in ["2", "вторая", "два"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"][
                                "text"] = f"{state.stateen['enemsecond']}, чтобы продолжить, скажите 'продолжить приключение'"
                            state.fights = 1
                            state.fight_step = 1
                            state.num.remove(n)
                    elif req["request"]["original_utterance"].lower() in ["3", "третья", "три"]:
                        if state.stateen["enem_hp"] > 0:
                            res["response"][
                                "text"] = f"Вы нанесли {state.atc} урона, готовьтесь к его атаке, чтобы продолжить скажите 'продолжить'"
                            state.fight_step = -1
                        else:
                            res["response"][
                                "text"] = f"{state.stateen['enemthird']}, чтобы продолжить, скажите 'продолжить приключение'"
                            state.fights = 1
                            state.fight_step = 1
                            state.num.remove(n)
                    else:
                        res["response"]["text"] = f"скажите, какую атаку вы хотите использовать один два или три, \n" \
                                                  f"чтобы посмотреть атаки, скажите 'способности рыцаря'"

                elif state.fight_step == -1:
                    if req["request"]["original_utterance"].lower() in ["продолжить", "дальше"]:
                        enem_atc = random.randint(state.stateen["enemmaxa"], state.stateen["enemmina"])
                        enem_atsh = random.randint(15, 20)
                        if enem_atsh >= state.state["shield"] and (state.state["hp"] + enem_atc) > 0:
                            res["response"][
                                "text"] = f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                          f"урона, теперь кидайте кубик щита" \
                                          f" напоминаю, чтобы пробить щит скажите 'пробить щит'"
                            state.state["hp"] = state.state["hp"] + enem_atc
                            state.fight_step = 2
                        elif enem_atsh >= state.state["shield"] and (state.state["hp"] + enem_atc) <= 0:
                            res["response"][
                                "text"] = f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                          f"урона, и к сожалению вы погибли..." \
                                          f" захотите поиграть еще, я всегда тут"
                            res["response"]["tts"] = f'<speaker audio="alice-sounds-game-loss-3.opus">'\
                                                      f"Враг выбросил {enem_atsh} и пробил ваш щит и нанёс вам {enem_atc} " \
                                                      f"урона, и к сожалению вы погибли..." \
                                                      f" захотите поиграть еще, я всегда тут"
                            res['response']['end_session'] = True
                            state.state = {}
                            state.etap = "askname"
                            state.fights = 0
                            state.fight_step = 1
                            state.num = [1, 3, 4, 6, 7, 8, 9, 10, 11, 13]

                        else:
                            res["response"][
                                "text"] = f"Враг выбросил {enem_atsh} и не пробил ваш щит теперь вы кидаете кубик щита" \
                                          f" напоминаю, чтобы пробить щит скажите 'пробить щит'"
                            state.fight_step = 2
                    else:
                        res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить'"

    elif state.etap == 'begin':
        if req["request"]["original_utterance"].lower() in ["продолжить", "дальше"]:
            res["response"]["text"] = "Хорошо! Чтобы отправиться в путь скажите 'начать приключение', состояние игрока можно проверить командой профиль "
            res["response"]["tts"] = '<speaker audio="alice-sounds-game-boot-1.opus"> Хорошо! Чтобы отправиться в путь ' \
                                    'скажите "начать приключение", состояние игрока можно проверить командой профиль '
            state.etap = 'fight'
        else:
            res["response"]["text"] = "Напоминаю, чтобы продолжить скажите 'продолжить'"

    elif state.etap == 'askrole':
        role = req["request"]["original_utterance"]
        state.state["role"] = role
        if role == "эльф":
            res["response"]["text"] = "Отлично! вы меткий эльф из лесов. \n Чтобы пройти дальше, скажите 'продолжить'"
            res["response"]["tts"] = '<speaker audio="alice-sounds-game-powerup-1.opus"> ' \
                                     'Отлично! вы меткий эльф из лесов. \n Чтобы пройти дальше, скажите "продолжить"'
            state.etap = 'begin'
            state.state["hp"] = 12
            state.state["shield"] = 17
            state.state["mina"] = 2
            state.state["maxa"] = 6
        elif role == "рыцарь":
            res["response"]["text"] = "Отлично! вы бесстрашный воин королевства. \n Чтобы пройти дальше, скажите 'продолжить'"
            res["response"]["tts"] = '<speaker audio="alice-sounds-game-powerup-1.opus"> ' \
                                     'Отлично! вы бесстрашный воин королевства. \n Чтобы пройти дальше, скажите "продолжить"'
            state.etap = 'begin'
            state.state["hp"] = 13
            state.state["shield"] = 17
            state.state["mina"] = 2
            state.state["maxa"] = 5
        elif role == "маг":
            res["response"]["text"] = "Отлично! вы мудрый чародей башни. \n Чтобы пройти дальше, скажите 'продолжить'"
            res["response"]["tts"] = '<speaker audio="alice-sounds-game-powerup-1.opus"> ' \
                                     'Отлично! вы мудрый чародей башни. \n Чтобы пройти дальше, скажите "продолжить"'
            state.etap = 'begin'
            state.state["hp"] = 11
            state.state["shield"] = 18
            state.state["mina"] = 2
            state.state["maxa"] = 6
        elif role == "варвар":
            res["response"]["text"] = "Отлично! вы грозный варвар из гор. \n Чтобы пройти дальше, скажите 'продолжить'"
            res["response"]["tts"] = '<speaker audio="alice-sounds-game-powerup-1.opus"> Отлично! вы грозный варвар из ' \
                                     'гор. \n Чтобы пройти дальше, скажите "продолжить"'
            state.etap = 'begin'
            state.state["hp"] = 14
            state.state["shield"] = 16
            state.state["mina"] = 2
            state.state["maxa"] = 7
        else:
            res["response"]["text"] = "Повторите роль ещё раз, напоминаю, у вас всего четыре варианта: эльф, маг, рыцарь или варвар"

    elif state.etap == 'checkname':
        if req["request"]["original_utterance"].lower() in ["да", "правильно"]:
            res["response"]["text"] = f'Приятно познокомиться, {state.state["name"]}. Теперь назовите персонажа, Для просмотра способностей определённого персонажа' \
                          ' скажите "какие способности у ..."'
            res["response"]["tts"] = f'<speaker audio="alice-sounds-game-boot-1.opus">'\
                          f'Приятно познокомиться, {state.state["name"]}. Теперь назовите персонажа, Для просмотра способностей определённого персонажа' \
                          ' скажите "какие способности у ..."'
            state.etap = 'askrole'
        elif req["request"]["original_utterance"].lower() in ["нет", "не правильно", "заново"]:
            res["response"]["text"] = 'Повторите имя, пожалуйста'
            res["response"]["tts"] = '<speaker audio="alice-sounds-game-boot-1.opus"> Повторите имя, пожалуйста'
            state.etap = 'askname'
        else:
            res["response"]["text"] = 'Так да или нет?'

    elif state.etap == 'askname':
        state.state["name"] = req["request"]["original_utterance"]
        res["response"]["text"] = f'Супер! Правильно ли я поняла, что вас зовут {state.state["name"]}?'
        res["response"]["tts"] = f'<speaker audio="alice-sounds-game-boot-1.opus">'\
                                 f'Супер! Правильно ли я поняла, что вас зовут {state.state["name"]}?'
        state.etap = 'checkname'

    res['user_state_update'] = state.to_dict()


if __name__ == '__main__':
    app.run()