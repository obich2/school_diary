import json
from excel_diary import all_classes
import pymorphy2
import datetime

current_time = datetime.datetime.now().time()
print(str(current_time) > '18:00')


def request_day_of_the_week(days: int):
    today = datetime.datetime.today()
    request_day = today + datetime.timedelta(days=days)
    return request_day.weekday() if 0 <= request_day.weekday() < 5 else False


def get_lesson_from_json(weekday: int, user_class, lesson_number, res):
    with open('diary.json', mode='r', encoding="UTF-8") as file:
        diary_dict = json.load(file)
        response_lesson = diary_dict['classes'][user_class][str(weekday)][lesson_number]  # ПЕРЕДЕЛАЙ ЭТОТ СТР
        res['response'][
            'text'] = f'Урок - {" ".join(response_lesson["subject"])}. Учитель - {" ".join(response_lesson["teacher"])}. Кабинет - {response_lesson["classroom"][1:-1]}'  # передалть джоины и сделать чтобы все было норм в джсоне


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
    lesson_number = slots.get('count', {}).get('value', '')
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
        print(when)
        request_day = request_day_of_the_week(when)
        print(request_day)
        print(request_day)
        if type(request_day) is not int:
            res['response']['text'] = 'УРААААА!!! В этот день не нужно идти в школу!'
            return
        else:
            get_lesson_from_json(request_day, user_class, lesson_number, res)
            return
    else:
        get_lesson_from_json(request_day_of_the_week(0), user_class, lesson_number, res)
        return

    res['response']['text'] = 'Я вас не поняла. Попробуйте перефразировать ваш вопрос?'


def get_diary(req, res):
    pass


def teacher_subject(req, res):
    pass


def unknown_command(req, res):
    res['response'][
        'text'] = 'Я навык, у которого вы можете получить различную информацию об обитателях 1259'  # переделать


def help_bot(req, res, fix):
    res['response']['text'] = 'Привет! Ответь на вопрос в каком ты классе, если ты еще не ответил. Если уже ответил, ' \
                              'то ты можешь спросить "Какой первый/второй/третий и так далее уроки". Пока что ' \
                              'функционал очень маленький'


def call_schedule(req, res, fix):
    res['response']['text'] = ('Первый урок: 8:30-9:15\nВторой урок: 9:30-10:15\nТретий урок: 10:30-11:15\nЧетвёртый '
                               'урок: 11:35-12:20\nПятый урок: 12:40-13:25\nШестой урок: 13:45-14:30\nСедьмой урок: '
                               '14:45-15:30\nВосьмой урок: 15:45-16:30')


def handle_dialog(req, res):
    intents = {
        "which_lesson": which_lesson,
        "get_diary": get_diary,
        "teacher_subject": teacher_subject,
        "help": help_bot,
        "call_schedule": call_schedule
    }
    user_id = req['session']['user_id']

    if req['session']['new']:
        res['response']['text'] = 'Привет, в каком ты классе?'
        return
    if res['session_state']['user_class'] == 0:
        for school_class in all_classes:
            if school_class in req['request']['original_utterance'].lower():
                res['session_state']['user_class'] = school_class
                res['response']['text'] = f'ООооо, так ты из {res["session_state"]["user_class"]}'
                return
    try:
        if res['session_state']['user_class'] == 0 and list(req['request']['nlu']['intents'].keys())[0] in [
            'which_lesson']:
            res['response'][
                'text'] = 'Чтобы узнать данную информацию, скажите для какого класса её получать, а потом повторите ' \
                          'этот запрос'
        else:
            intents[list(req['request']['nlu']['intents'].keys())[0]](req, res, res['session_state']['user_class'])
    except IndexError:
        unknown_command(req, res)
