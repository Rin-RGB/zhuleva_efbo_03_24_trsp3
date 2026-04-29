# Контрольная работа №3
Выполнила Жулева Дарья, ЭФБО-03-24

## Инструкция по запуску
1. Клонировать репозиторий: `git clone https://github.com/Rin-RGB/zhuleva_efbo_03_24_trsp3.git`

2. Создать и активировать виртуальное окружение:

### Windows
python -m venv venv  
venv\Scripts\activate

### Mac/Linux
python3 -m venv venv  
source venv/bin/activate


3. Установить зависимости  
pip install -r requirements.txt  

4. Запуск  

### Задание 6.1  
uvicorn 6-1:app --reload --port 8001  

### Задание 6.2  
uvicorn 6-2:app --reload --port 8002  

### Задание 6.3  
uvicorn 6-3:app --reload --port 8003  

### Задание 6.4  
uvicorn 6-4:app --reload --port 8004  

### Задание 6.5  
uvicorn 6-5:app --reload --port 8005  

### Задание 7.1  
uvicorn 7-1:app --reload --port 8006

### Задание 8.1  
uvicorn 8-1:app --reload --port 8007  

### Задание 8.2  
uvicorn 8-2:app --reload --port 8008  

# Тестирование
Тестирование 6.1
При переходе в http://127.0.0.1:8000/login возникает окошко. Если ввести корректные данные 
`user1` и `pass1`, то выйдет сообщение {"message":"You got my secret, welcome"}
![окошко для входа](img/login.png)

При вводе неверных данных открывает окошко ещё раз
___

Тестирование 6.2

```curl -X POST -H "Content-Type: application/json" -d "{\"username\":\"user1\",\"password\":\"correctpass\"}" http://localhost:8000/register```

Результат: {"message":"User registered successfully"}


```curl -u user1:correctpass http://localhost:8000/login```

Результат: {"message":"Welcome, user1"}

```curl -u user1:wrongpass http://localhost:8000/login```

Результат: {"detail":"Invalid credentials"}
___
Тестирование 6.3

При MODE=DEV

```curl -u wrong_user:wrong_password http://localhost:8000/docs```
Результат: {"detail":"Unauthorized"}

```curl -i -u admin:secret http://localhost:8000/docs```
Результат: документация в формате html

При MODE=PROD

```curl http://localhost:8000/docs```
Результат: {"detail":"Not Found"}
___
Тестирование 6.4

Проверка на http://127.0.0.1:8000/docs

При попытке login с неверными данными выдаёт ```{
  "detail": "Invalid credentials"
}```

При попытке получить данные без токена выдаёт ```{
  "detail": "Not authenticated"
}```

При вводе верных данных возвращает токен. При авторизации и попытке получить защищённые данные возвращает ```{
  "message": "Access granted"
}```
___
Тестирование 6.5

При регистрации нового пользователя появляется ```{
  "message": "New user created"
}```

При попытке регистрировать того же пользователя ошибка 409 ```{
  "detail": "User already exists"
}```

При попытке зарегистрировать пользователя сразу после первого ```{
  "error": "Rate limit exceeded: 1 per 1 minute"
}```

При неправильных вводных данных ошибка 401 ```{
  "detail": "Authorization failed"
}```

При неправильном username в логине ошибка 404 ```{
  "detail": "User not found"
}```

При логине этого пользователя появляется токен

Без логина попытка получить защищённые данные вызывает ошибку 401

При попытке получить защищённые данные после авторизации ```{
  "message": "Access granted"
}```
___
Тестирование 7.1

При попытке выполнить любой запрос без авторизации результат: ```{
  "detail": "Not authenticated"
}```

При входе со стороны гостя `guest` и `guestpass` мы можем получить public recources: ```{
  "message": "Public resources read by guest",
  "role": [
    "guest"
  ]
}```

При входе со стороны пользователя можно просмотреть ресурсы либо обновить их. При попытке обновить появляется: ```{
  "message": "Resource 1 updated by user",
  "role": [
    "user",
    "guest"
  ]
}```

Со стороны администратора можно выполнить любой запрос. Чтобы аойти как администратор нужно использовать логин `admin` и `adminpass`
___
Тестирование 8.1

При попытке получить пользователей до регистрации первого пользователя результат: ```{
  "users": []
}```

После регистрации в пользователях появляется: ```{
  "users": [
    {
      "id": 1,
      "username": "alice"
    }
  ]
}```

Если запросить пользователя с несуществующим id: ```{
  "detail": "User not found"
}```

Если запросить пользователя с существующим id: ```{
  "id": 1,
  "username": "alice"
}```
---
Тестирование 8.2

При выполнении post: ```{
  "id": 1,
  "title": "todo",
  "description": "need to do",
  "completed": false,
  "created_at": "2026-04-29 12:22:04"
}```

При выполнении put: ```{
  "id": 1,
  "title": "new",
  "description": "new_description",
  "completed": true,
  "created_at": "2026-04-29 12:22:04"
}```

При выполнении get всех задач: ```[
  {
    "id": 2,
    "title": "todo2",
    "description": "need to do too",
    "completed": false,
    "created_at": "2026-04-29 12:30:39"
  },
  {
    "id": 1,
    "title": "new",
    "description": "new_description",
    "completed": true,
    "created_at": "2026-04-29 12:22:04"
  }
]```

При выполнении любого запроса с несуществующим id: ```{
  "detail": "Todo not found"
}```

При удалении todo возвращает статус 204 без тела.