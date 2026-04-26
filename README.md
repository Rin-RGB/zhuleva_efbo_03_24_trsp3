Тестирование 6.2
---
```curl -X POST -H "Content-Type: application/json" -d "{\"username\":\"user1\",\"password\":\"correctpass\"}" http://localhost:8000/register```

Результат: {"message":"User registered successfully"}


```curl -u user1:correctpass http://localhost:8000/login```

Результат: {"message":"Welcome, user1"}

```curl -u user1:wrongpass http://localhost:8000/login```

Результат: {"detail":"Invalid credentials"}

Тестирование 6.3
---
При MODE=DEV

```curl -u wrong_user:wrong_password http://localhost:8000/docs```
Результат: {"detail":"Unauthorized"}

```curl -i -u admin:secret http://localhost:8000/docs```
Результат: документация в формате html

```curl http://localhost:8000/docs```
Результат: {"detail":"Not Found"}

Тестирование 6.4
---




