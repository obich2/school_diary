def which_lesson(req, res):
    pass


def get_diary(req, res):
    pass


def teacher_subject(req, res):
    pass


def unknown_command(req, res):
    res['response'][
        'tetx'] = 'Я навык, у которого вы можете получить различную информацию об обитателях 1259'  # переделать


def hanlder(event, context):
    intents = {
        "which_lesson": which_lesson,
        "get_diary": get_diary,
        "teacher_subject": teacher_subject
    }
    response = {
        'session': event['session'],
        'version': event['version'],
        'response': {
            'end_session': False
        },
        'session_state': event.get('state', {}).get('session', {})
    }