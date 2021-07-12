# Описание API

Все вызовы API принимают и отдают JSON-данные.

## Для администратора

Все вызовы для администратора требуют базовую HTTP-авторизацию.

#### GET /admin/polls

Получение списка всех опросов. Тело ответа:
```
[
    {
        id,             # Число
        name,           # Строка
        description,    # Строка
        startDate,      # Формат YYYY-MM-DD
        finishDate      # Формат YYYY-MM-DD
    },
    ...
]
```

#### POST /admin/polls

Создание нового опроса. Тело запроса:
```
{
    name,           # Строка
    description,    # Строка
    startDate,      # Строка YYYY-MM-DD
    finishDate      # Строка YYYY-MM-DD
}
```
Тело ответа:
```
{
    id, name, description, startDate, finishDate
}
```

#### GET /admin/polls/(id)

Получение подробной информации об одном опросе, с вопросами и ответами.
Тело ответа:
```
{
    id, 
    name,           # Строка
    description,    # Строка
    startDate,      # Строка YYYY-MM-DD
    finishDate      # Строка YYYY-MM-DD
    questions: [
        {
            id,
            text,           # Текст вопроса
            type,           # Тип вопроса: TEXT, CHOICE, MULTIPLE_CHOICE
            options: [      # Список вариантов (только для типов CHOICE, MULTIPLE_CHOICE)
                { id, index, text },
                ...
            ]
        },
        ...
    ]
}

```

#### DELETE /admin/polls/(id)

Удаление опроса.

#### PATCH /admin/polls/(id)

Редактирование опроса. Тело запроса (все поля опциональные):
```
{
    name,           # Строка
    description,    # Строка
    finishDate      # Строка YYYY-MM-DD
}
```
Формат ответа:
```
{
    id, name, description, startDate, finishDate
}
```

#### POST /admin/polls/(id)/questions

Добавление нового вопроса к опросу id. Тело запроса:
```
{
    text,           # Текст вопроса
    type,           # Тип вопроса: TEXT, CHOICE, MULTIPLE_CHOICE
    options: [      # Список вариантов (только для типов CHOICE, MULTIPLE_CHOICE)
        'Вариант 1',
        'Вариант 2',
        ...
    ]
}
```
Тело ответа:
```
{
    id,
    text,           # Текст вопроса
    type,           # Тип вопроса: TEXT, CHOICE, MULTIPLE_CHOICE
    options: [      # Список вариантов (только для типов CHOICE, MULTIPLE_CHOICE)
        { id, index, text },
        ...
    ]
}
```

#### GET /admin/polls/(pollId)/questions/(questionId)

Подробная информация об одном вопросе. Тело ответа:
```
{
    id,
    text,           # Текст вопроса
    type,           # Тип вопроса: TEXT, CHOICE, MULTIPLE_CHOICE
    options: [      # Список вариантов (только для типов CHOICE, MULTIPLE_CHOICE)
        { id, index, text },
        ...
    ]
}
```

#### DELETE /admin/polls/(pollId)/questions/(questionId)

Удаление вопроса из опроса.

#### PATCH /admin/polls/(pollId)/questions/(questionId)

Изменение существующего вопроса. Тело запроса (все поля опциональные):
```
{
    text,           # Текст вопроса
    type,           # Тип вопроса: TEXT, CHOICE, MULTIPLE_CHOICE
    options: [      # Список вариантов (только для типов CHOICE, MULTIPLE_CHOICE)
        'Вариант 1',
        'Вариант 2',
        ...
    ]
}
```
Тело ответа:
```
{
    id,
    text,           # Текст вопроса
    type,           # Тип вопроса: TEXT, CHOICE, MULTIPLE_CHOICE
    options: [      # Список вариантов (только для типов CHOICE, MULTIPLE_CHOICE)
        { id, index, text },
        ...
    ]
}
```


## Для пользователя

#### GET /polls

Получить список активных опросов. Тело ответа:
```
[
    {
        id,             # Число
        name,           # Строка
        description,    # Строка
        startDate,      # Формат YYYY-MM-DD
        finishDate      # Формат YYYY-MM-DD
    },
    ...
]
```

#### GET /polls/(id)

Получение подробной информации об одном опросе, с вопросами и ответами.
Тело ответа:
```
{
    id, 
    name,           # Строка
    description,    # Строка
    startDate,      # Строка YYYY-MM-DD
    finishDate,     # Строка YYYY-MM-DD
    questions: [
        {
            id,
            text,           # Текст вопроса
            type,           # Тип вопроса: TEXT, CHOICE, MULTIPLE_CHOICE
            options: [      # Список вариантов (только для типов CHOICE, MULTIPLE_CHOICE)
                { index, text },
                ...
            ]
        },
        ...
    ]
}
```

#### POST /polls/(pollId)

Прохождение опроса пользователем. Тело запроса:
```
{
    userId,     # Идентификатор пользователя
    answers: {
        'questionId1': 'Free answer',       # Для type=TEXT
        'questionId2': optionIndex,         # Для type=CHOICE
        'questionId3': [optionIndex, ...],  # Для type=MULTIPLE_CHOICE
        ...
    }
}
```

#### GET /pollsByUser/(userId)

Получить пройденные пользователем опросы, с детализацией выбранных ответов.
Тело ответа:
```
[
    {
        id,                 # Идентификатор заполненного опроса
        submitTime,         # Дата и время прохождения опроса, формат YYYY-MM-DDThh:mm:ss
        pollId,             # Идентификатор опроса
        answers: [
            {
                question: {                 # Описание вопроса
                    id,                     # Идентификатор вопроса
                    type,                   # Тип вопроса: TEXT, CHOICE, MULTIPLE_CHOICE
                    text,                   # Текст вопроса, на момент прохождения
                },
                answer: 'Text',             # Для type=TEXT, CHOICE
                answer: ['Option', ...]     # Для type=MULTIPLE_CHOICE
            },
            ...
        ]
    },
    ...
]
```
