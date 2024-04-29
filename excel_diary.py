# import module
import time
from teachers_dict import teachers_dict
import openpyxl
import json

# load excel with its path

answer = {
    "classes": {

    },
    "teachers": {
        'Антипова Мария Юрьевна': ['Р', 'Л'],
        'Третьякова Елена Геннадьевна': ['Р', 'Л'],
        'Худойназарова Алла Геннадьевна': ['Р', 'Л'],
        'Никитина Полина Валерьевна': ['Р', 'Л'],
        'Гончарова Лариса Михайловна': ['Р', 'Л'],
        'Комарова Галина Анатольевна': ['Р', "Л"],
        "Салюкова Наталья Вячеславовна": ['Р', "Л"],
        "Шилкина Стелла Львовна": ["Р", "Л"],
        "Артемова Мария Владиславовна": ["М"],
        "Корсакова Татьяна Николаевна": ["М"],
        "Ворожейкин Сергей Евгеньевич": ["М"],
        "Емельянова Евгения Валерьевна": ["М"],
        "Кунденок Елена Анатольевна": ["М"],
        "Уланова Ольга Олеговна": ["Ф"],
        "Бурдина Ирина Борисовна": ['Ф', 'М'],
        "Головнер Владимир Нодарович": ['Х'],
        "Хохлова Людмила Васильевна": ['Б'],
        'Кузнецов Анатолий Евгеньевич': ['ИКТ'],
        'Горшкова Маргарита Владимировна': ['ИКТ'],
        'Бондаренко Елена Юрьевна': ['Б', 'Х'],
        'Галкина Елена Витальевна': ['Б'],
        'Колегова Марина Александровна': ['И', "О"],
        'Макарчук Николай Евгеньевич': ['И'],
        'Колосова Марина Николаевна': ['И', 'О'],
        'Кунгурцев Роман Александрович': ['И', "О"],
        "Мельникова Антонина Николаевна": ['Г'],
        "Говорова Марина Владимировна": ['И', "О"],
        'Бобровская Наталья Анатольевна': ['А'],
        "Камышанова Анна Владимировна": ['А'],
        "Бойкова Светлана Геннадьевна": ['А'],
        "Волкова Наталья Вадимовна": ['А'],
        "Карпачева М.В.": ['А'],
        "Сиверкина Диана Александровна": ['А'],
        "Саммель Регина Анатольевна": ["А"],
        "Марченко Элла Михайловна": ["А"],
        "Жучкова Надежда Александровна": ["А"],
        "Пестравкина Ольга Георгиевна": ["А"],
        "Хареми Людмила Вячеславовна": ["А"],
        "Смирнова Светлана Борисовна": ["Г"],
        "Елистратов Александр Александрович": ['Физра', 'ОБЖ'],
        "Курышев Михаил Юрьевич": ["Физра"],
        "Кудряшов Иван Валерьевич": ["Физра"],
        "Буганина И.Ю.": ["Труд"],
        'Хохлова Л.А.': ['U'],
        'Павлова Ольга Анатольевна': ['Математика'],
        'Берсенева Елена Михайловна': ['Английский язык'],
        'Лушникова Т.Б.': ['Биология']
    }
}


def add_class_to_dict(class_name):
    answer["classes"][class_name] = {
        "Понедельник": [{"subject": "", "teacher": "", "classroom": ""} for n in range(1, 9)],
        "Вторник": [{"subject": "", "teacher": "", "classroom": ""} for n in range(1, 8)],
        "Среда": [{"subject": "", "teacher": "", "classroom": ""} for n in range(1, 8)],
        "Четверг": [{"subject": "", "teacher": "", "classroom": ""} for n in range(1, 8)],
        "Пятница": [{"subject": "", "teacher": "", "classroom": ""} for n in range(1, 8)]
    }


def insert_lesson_data(current_school_class, current_day, lesson_data, lesson_number):
    print(current_school_class, current_day, lesson_data)
    subject = ''
    classroom = ''
    teacher = ''
    if current_school_class != 'УПК':
        days_of_the_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]

        for i, j in enumerate(lesson_data):
            if j[0] == '(':
                subject = lesson_data[:i]
                classroom = lesson_data[i]
                teacher = lesson_data[i+1:]
                break
        lesson = answer["classes"][current_school_class][days_of_the_week[current_day]][
            lesson_number - 1]  # мб изменить и ускорить алгоритм
        lesson['subject'] = subject
        lesson['classroom'] = classroom
        lesson['teacher'] = teacher


# iterate through excel and display data
wrkbk = openpyxl.load_workbook("diary_files/Diary.xlsx")
ws = wrkbk.active
filled_columns = [i.coordinate for i in list(ws.rows)[0]][2:]


current_school_class = ''
ws2 = wrkbk.active
for column in filled_columns:
    for index, cell in enumerate(ws2[column[:-1]]):
        if index == 0:
            current_school_class = cell.value
            print(cell.value)
            current_day = -1
            add_class_to_dict(current_school_class)
        else:
            if cell.value is not None and cell.value != 'УПК':
                lesson_data = cell.value.split()
                lesson_number = index % 8
                if lesson_number == 1:
                    current_day += 1
                insert_lesson_data(current_school_class, current_day, lesson_data, lesson_number)

with open("diary.json", "w", encoding="utf-8") as file:
    json.dump(answer, file, ensure_ascii=False, indent=2)
