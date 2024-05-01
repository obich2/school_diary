import json

import pymorphy2
import datetime
current_time = datetime.datetime.now().time()
print(str(current_time) > '18:00')
def request_day_of_the_week(days: int):
    today = datetime.datetime.today()
    request_day = today + datetime.timedelta(days=days)
    return request_day.weekday() if  0 <= request_day.weekday() < 5 else False


def which_lesson(req, res, user_class):
    # count_to_lesson = {
    #     'первый': 0,
    #     'второй': 1,
    #     'третий': 2,
    #     'четвёртый': 3,
    #     'пятый': 4,
    #     'шестой': 5,
    #     'седьмой': 6,
    #     'восьмой': 7
    # }
    next_to_lesson = {
        'следующий': 1,
        'последний': -1,

    }

    slots = req['request']['nlu']['intents']['which_lesson']['slots']
    next = slots.get('next', {}).get('value', '')
    lesson_number = slots.get('lesson_number', {}).get('value', '')
    when = slots.get('when', {}).get('value', '')
    if next:
        next = next_to_lesson[next]
    if lesson_number:
        for i in req['request']['nlu']['tokens']:
            if i.isdigit():
                lesson_number = int(i) - 1

        # lesson_number = word_to_count[lesson_number]
        # morph = pymorphy2.MorphAnalyzer()                 // мб мне не понадобиться pymorphy потому что,
        # у меня в запросе будут только первый, второй и так далее lesson_number = morph.parse(lesson_number)[0].normal_form
    if when:
        for i in req['request']['nlu']['entities']:
            if i['type'] == 'YANDEX.DATETIME':
                when = i['value']['day']
        request_day = request_day_of_the_week(when)
        if not request_day:
            res['response']['text'] = 'УРААААА!!! Завтра не нужно идти в школу!'
            return
    else:
        request_day = request_day_of_the_week(0)
    with open('diary.json', mode='r', encoding="UTF-8") as file:
        diary_dict = json.load(file)
        response_lesson = diary_dict['classes'][user_class][lesson_number]
        res['response']['text'] = response_lesson
        return

    res['response']['text'] = 'Я вас не поняла. Попробуйте перефразировать ваш вопрос?'


def get_diary(req, res):
    pass


def teacher_subject(req, res):
    pass


def unknown_command(req, res):
    res['response'][
        'text'] = 'Я навык, у которого вы можете получить различную информацию об обитателях 1259'  # переделать


def handle_dialog(req, res):
    intents = {
        "which_lesson": which_lesson,
        "get_diary": get_diary,
        "teacher_subject": teacher_subject
    }
    user_id = req['session']['user_id']

    if req['session']['new']:
        res['response']['text'] = 'Привет, в каком ты классе?'
        return
    if res['session_state']['user_class'] == 0:
        for school_class in ['10и']:
            if school_class in req['request']['original_utterance'].lower():
                res['session_state']['user_class'] = school_class
                res['response']['text'] = f'ООооо, так ты из {res["session_state"]["user_class"]}'
                return
    try:
        if res['session_state']['user_class'] == 0 and list(req['request']['nlu']['intents'].keys())[0] in ['which_lesson']:
            res['response']['text'] = 'Чтобы узнать данную информацию, скажите для какого класса её получать, а потом повторите этот запрос'
        else:
            intents[list(req['request']['nlu']['intents'].keys())[0]](req, res, res['session_state']['user_class'])
    except IndexError:
        unknown_command(req, res)