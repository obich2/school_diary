import json
from excel_diary import all_classes
import pymorphy2
import datetime

current_time = datetime.datetime.now().time()
number_to_string = {
    0: 'первый',
    1: 'второй',
    2: 'третий',
    3: 'четвертый',
    4: 'пятый',
    5: 'шестой',
    6: 'седьмой',
    7: 'восьмой',
    8: 'девятый'
}


def request_day_of_the_week(days: int, month=0):
    today = datetime.datetime.today()
    if month:
        current_year = today.year
        request_date = datetime.datetime(current_year, month, days)
    else:
        today = datetime.datetime.today()
        request_date = today + datetime.timedelta(days=days)
    return request_date.weekday() if 0 <= request_date.weekday() < 5 else False


def get_lesson_from_json(weekday: int, user_class, lesson_number, res):
    if lesson_number is None:
        with open('diary.json', mode='r', encoding="UTF-8") as file:
            diary_dict = json.load(file)

            for i in range(0, 8):
                response_lesson = diary_dict['classes'][user_class][str(weekday)][i]  # ПЕРЕДЕЛАЙ ЭТОТ СТР
                if response_lesson['subject']:
                    res['response'][
                        'text'] = res['response'].get('text', '') + f'{number_to_string[i].capitalize()} урок - {" ".join(response_lesson["subject"])}. Учитель - {" ".join(response_lesson["teacher"])}. Кабинет - {response_lesson["classroom"][1:-1]}\n'  # передалть джоины и сделать чтобы все было норм в джсоне
                else:
                    res['response'][
                        'text'] = res['response'].get('text',
                                                      '') + f'{number_to_string[i].capitalize()} урок - нет\n'  # передалть джоины и сделать чтобы все было норм в джсоне
    else:
        with open('diary.json', mode='r', encoding="UTF-8") as file:
            diary_dict = json.load(file)
            print(user_class, weekday, lesson_number)
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
    string_to_number = {
        'перв': 0,
        'втор': 1,
        'трет': 2,
        'четверт': 3,
        'пят': 4,
        'шест': 5,
        'седьм': 6,
        'восьм': 7,
        'девят': 8
    }
    slots = req['request']['nlu']['intents']['which_lesson']['slots']
    next = slots.get('next', {}).get('value', '')
    lesson_number = slots.get('count', {}).get('value', '')
    when = slots.get('when', {}).get('value', '')
    if next:
        next = next_to_lesson[next]
    if lesson_number:
        lesson_number = string_to_number[lesson_number[:-2]]
        # lesson_number = word_to_count[lesson_number]
        # morph = pymorphy2.MorphAnalyzer()                 // мб мне не понадобиться pymorphy потому что,
        # у меня в запросе будут только первый, второй и так далее lesson_number = morph.parse(lesson_number)[0].normal_form
    if when:
        for i in req['request']['nlu']['entities']:
            if i['type'] == 'YANDEX.DATETIME':
                if i['value']['day_is_relative']:
                    when = i['value']['day']
                    request_day = request_day_of_the_week(when)

                else:
                    day = i['value']['day']
                    month = i['value']['month']
                    request_day = request_day_of_the_week(day, month)

                break
        if request_day is False:
            res['response']['text'] = 'УРААААА!!! В этот день не нужно идти в школу!'
            return
        else:
            get_lesson_from_json(request_day, user_class, lesson_number, res)
            return
    else:
        request_day = request_day_of_the_week(0)
        if 0 <= request_day >= 4:
            get_lesson_from_json(request_day_of_the_week(0), user_class, lesson_number, res)
        else:
            res['response']['text'] = 'УРААААА!!! В этот день не нужно идти в школу!'
        return


def get_diary(req, res, user_class):
    slots = req['request']['nlu']['intents']['get_diary']['slots']
    when = slots.get('when', {}).get('value', '')
    lesson_number = None
    # lesson_number = word_to_count[lesson_number]
    # morph = pymorphy2.MorphAnalyzer()                 // мб мне не понадобиться pymorphy потому что,
    # у меня в запросе будут только первый, второй и так далее lesson_number = morph.parse(lesson_number)[0].normal_form
    if when:
        for i in req['request']['nlu']['entities']:
            if i['type'] == 'YANDEX.DATETIME':
                if i['value']['day_is_relative']:
                    when = i['value']['day']
                    request_day = request_day_of_the_week(when)

                else:
                    day = i['value']['day']
                    month = i['value']['month']
                    request_day = request_day_of_the_week(day, month)

                break
        if request_day is False:
            res['response']['text'] = 'УРААААА!!! В этот день не нужно идти в школу!'
            return
        else:
            get_lesson_from_json(request_day, user_class, lesson_number, res)
            return
    else:
        request_day = request_day_of_the_week(0)
        if 0 <= request_day >= 4:
            get_lesson_from_json(request_day_of_the_week(0), user_class, lesson_number, res)
        else:
            res['response']['text'] = 'УРААААА!!! В этот день не нужно идти в школу!'
        return


def teacher(req, res, fix):
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
        "teacher": teacher,
        "help": help_bot,
        "call_schedule": call_schedule
    }
    user_id = req['session']['user_id']

    if req['session']['new']:
        res['response']['text'] = 'Привет, в каком ты классе?'
        return
    if res['session_state']['user_class'] == 0:
        for school_class in ['5а', '5б', '5в', '5г', '5д', '6а', '6б', '6в', '6г', '6д', '7а', '7б', '7г', '7м', '8а',
                             '8б', '8в', '8г', '8м', '9а', '9в', '9г', '9м', '10а', '10и', '10ф', '11а', '11г', '11ф']:
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
