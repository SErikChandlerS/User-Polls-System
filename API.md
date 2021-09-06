# Api description

All requests accept json-data.

## For administrator

All calls to the administrator require basic HTTP authorization.

#### GET /admin/polls

Getting a list of all surveys. Response body:
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


Creating a new survey. Request Body:
```
{
    name,           # Строка
    description,    # Строка
    startDate,      # Строка YYYY-MM-DD
    finishDate      # Строка YYYY-MM-DD
}
```
Response body:
```
{
    id, name, description, startDate, finishDate
}
```

#### GET /admin/polls/(id)

Getting detailed information about a single survey, with questions and answers.
Response body:
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

Poll delete.

#### PATCH /admin/polls/(id)

Editing the poll. Request body (all fields are optional):
```
{
    name,           # Строка
    description,    # Строка
    finishDate      # Строка YYYY-MM-DD
}
```
Response format:
```
{
    id, name, description, startDate, finishDate
}
```

#### POST /admin/polls/(id)/questions

Adding a new question to the survey id. Request Body:
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
Response body:
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

Detailed information about one question. Response body:
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

Deleting a question from the survey.

#### PATCH /admin/polls/(pollId)/questions/(questionId)

Edit an existing question. Request body (all fields are optional):
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
Response body:
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

Get a list of active surveys. Response body:
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

Getting detailed information about a single survey, with questions and answers.
Response body:
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

Passing the survey by the user. Request Body:
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


Survey completion Get the surveys completed by the user, with details of the selected responses.
Response body:
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
