from requests import get, delete

#  API ля таблицы users
#  получение информации о пользователе/пользователях
print(get('http://localhost:8080/api/users').json())  # получение всех пользователей
print(get('http://localhost:8080/api/users/2').json())  # корректное получение одного пользователя по id
print(get('http://localhost:8080/api/users/').json())  # ошибочный запрос - пустой
print(get('http://localhost:8080/api/users/999').json())  # ошибочный запрос - нет такого id
print(get('http://localhost:8080/api/users/belka').json())  # ошибочный запрос - строка
print()
# удаление пользователя по id
print(delete('http://localhost:8080/api/users/').json())  # ошибочный запрос - пустой
print(delete('http://localhost:8080/api/users/999').json())  # ошибочный запрос - нет такого id
print(delete('http://localhost:8080/api/users/belka').json())  # ошибочный запрос - строка
print(delete('http://localhost:8080/api/users/3').json())  # корректный запрос на удаление
print()
# API для таблицы ideas
# получение информации о идее/идеях
print(get('http://localhost:8080/api/ideas').json())  # получение всех идей
print(get('http://localhost:8080/api/ideas/2').json())  # корректное получение одной идеи по id
print(get('http://localhost:8080/api/ideas/').json())  # ошибочный запрос - пустой
print(get('http://localhost:8080/api/ideas/999').json())  # ошибочный запрос - нет такого id
print(get('http://localhost:8080/api/ideas/button').json())  # ошибочный запрос - строка
# удаление идеи по id
print(delete('http://localhost:8080/api/ideas/').json())  # ошибочный запрос - пустой
print(delete('http://localhost:8080/api/ideas/999').json())  # ошибочный запрос - нет такого id
print(delete('http://localhost:8080/api/ideas/belka').json())  # ошибочный запрос - строка
print(delete('http://localhost:8080/api/ideas/4').json())  # корректный запрос на удаление
# API для таблицы object
# получение информации о компоненте/компонентах
print(get('http://localhost:8080/api/objects').json())  # получение всех компонентов
print(get('http://localhost:8080/api/objects/2').json())  # корректное получение одного компонента по id
print(get('http://localhost:8080/api/objects/').json())  # ошибочный запрос - пустой
print(get('http://localhost:8080/api/objects/999').json())  # ошибочный запрос - нет такого id
print(get('http://localhost:8080/api/objects/alert').json())  # ошибочный запрос - строка
# удаление идеи по id
print(delete('http://localhost:8080/api/objects/').json())  # ошибочный запрос - пустой
print(delete('http://localhost:8080/api/objects/999').json())  # ошибочный запрос - нет такого id
print(delete('http://localhost:8080/api/objects/alert').json())  # ошибочный запрос - строка
print(delete('http://localhost:8080/api/objects/2').json())  # корректный запрос на удаление
# API для таблиц property и properties_values
# получение информации о свойстве/свойствах
print(get('http://localhost:8080/api/objects').json())  # получение всех свойств
print(get('http://localhost:8080/api/objects/2').json())  # корректный запрос на получение одного свойства по id и всех его значений
print(get('http://localhost:8080/api/objects/').json())  # ошибочный запрос - пустой
print(get('http://localhost:8080/api/objects/999').json())  # ошибочный запрос - нет такого id
print(get('http://localhost:8080/api/objects/color').json())  # ошибочный запрос - строка
