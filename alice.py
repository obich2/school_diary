def which_lesson(req, res):
    res['response']['text'] = 'УРА РАБОТАЕТ'


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
    if res['response']['session_state']['user_class'] == 0:
        for school_class in ['10и']:
            if school_class in req['request']['original_utterance'].lower():
                res['response']['session_state']['user_class'] = school_class
                res['response']['text'] = f'ООооо, так ты из {res["response"]["session_state"]["user_class"]}'
                return
    try:
        if res['response']['session_state']['user_class'] == 0 and list(req['request']['nlu']['intents'].keys())[0] in ['which_lesson']:
            res['response']['text'] = 'Чтобы узнать данную информацию, скажите для какого класса её получать, а потом повторите этот запрос'
        else:
            intents[list(req['request']['nlu']['intents'].keys())[0]](req, res)
    except IndexError:
        unknown_command(req, res)
