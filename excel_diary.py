# import module
import time
from teachers_dict import teachers_dict
import openpyxl

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


def insert_lesson_data(current_school_class, current_day, lesson_data):
    days_of_the_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]
    subject = lesson_data[0]
    try:
        classrom = lesson_data[1]
    except Exception as e:
        print(current_school_class, current_day, lesson_data)
    teacher = lesson_data[2:]
    lesson_number = counter // 8
    if lesson_number == 1:
        current_day += 1
    lesson = answer["classes"][current_school_class][days_of_the_week[current_day]][
        lesson_number - 1]  # мб изменить и ускорить алгоритм
    lesson['lesson'] = subject
    lesson['classrom'] = classrom
    lesson['teacher'] = teacher


# iterate through excel and display data
wrkbk = openpyxl.load_workbook("diary_files/Diary2.xlsx")
ws = wrkbk.active
filled_columns = [i.coordinate for i in list(ws.rows)[0]][2:]


counter = 0
current_day = -1
current_school_class = ''
ws2 = wrkbk.active
for column in filled_columns:
    for cell in ws2[column[:-1]]:
        if counter % 40 == 0:
            current_school_class = cell.value
            add_class_to_dict(current_school_class)
        else:
            if cell.value is not None and cell.value != 'УПК':
                lesson_data = cell.value.split()
                lesson_number = counter % 8
                if lesson_number == 1:
                    current_day += 1
                insert_lesson_data(current_school_class, current_day, lesson_data)
        counter += 1


# for row in ws.iter_rows(min_row=3, max_col=37, min_col=2, max_row=51, values_only=True):
#     teacher = row[0]
#     day_of_the_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]
#     day = -1
#     for index, current_school_class in enumerate(row[1:]):
#         if index % 7 == 0:
#             day += 1
#         if current_school_class:
#             if len(current_school_class) <= 3:
#                 if current_school_class not in answer["classes"]:
#                     answer["classes"][current_school_class] = {
#                         "Понедельник": {n: "" for n in range(1, 9)},
#                         "Вторник": {n: "" for n in range(1, 8)},
#                         "Среда": {n: "" for n in range(1, 8)},
#                         "Четверг": {n: "" for n in range(1, 8)},
#                         "Пятница": {n: "" for n in range(1, 8)}
#                     }
#                 else:
#                     if day == 0 and index % 7 == 1:
#                         answer['classes'][current_school_class][day_of_the_week[day]][index % 7] = 'Разговоры о важном'
#                     answer['classes'][current_school_class][day_of_the_week[day]][index % 7 + 1] = teachers_dict[teacher][0]
#             else:
#                 divided_class = current_school_class.split(', ')
#                 for i in divided_class:
#                     if i not in answer["classes"]:
#                         answer["classes"][i] = {
#                             "Понедельник": {n: "" for n in range(1, 9)},
#                             "Вторник": {n: "" for n in range(1, 8)},
#                             "Среда": {n: "" for n in range(1, 8)},
#                             "Четверг": {n: "" for n in range(1, 8)},
#                             "Пятница": {n: "" for n in range(1, 8)}
#                         }
#                     else:
#                         if day == 0 and index % 7 == 1:
#                             answer['classes'][i][day_of_the_week[day]][index % 7] = 'Разговоры о важном'
#                         answer['classes'][i][day_of_the_week[day]][index % 7 + 1] = teachers_dict[teacher][0]
print(answer)
