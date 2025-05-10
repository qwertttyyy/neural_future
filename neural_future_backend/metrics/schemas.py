from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiResponse

user_answer_create_schema = {
    'summary': 'Создать список ответов на вопросы',
    'description': (
        'Позволяет авторизованному пользователю отправить **список ответов** на вопросы. '
        'Если ответ на вопрос уже существует — он будет обновлён. '
        'Если нет — будет создан новый. Один вопрос — один ответ от пользователя.\n\n'
        '**Требуется авторизация.**'
    ),
    'examples': [
        OpenApiExample(
            name='Пример запроса',
            summary='Отправка списка ответов на три вопроса',
            description='Каждый объект содержит ID вопроса и текст ответа. ID пользователя не передаётся — он берётся из авторизации.',
            value=[
                {"question": 1, "answer": "Меня зовут Михаил"},
                {"question": 2, "answer": "25"},
                {"question": 3, "answer": "Из Москвы"},
            ],
            request_only=True,
        ),
        OpenApiExample(
            name='Пример успешного ответа',
            summary='Ответ с созданными/обновлёнными объектами',
            value=[
                {
                    "id": 1,
                    "answer": "Меня зовут Михаил",
                },
                {
                    "id": 2,
                    "answer": "25",
                },
                {
                    "id": 3,
                    "answer": "Из Москвы",
                },
            ],
            response_only=True,
        ),
        OpenApiExample(
            name='Пример ошибки валидации',
            summary='Ошибка из-за повторяющихся вопросов или неверных данных',
            value={
                "non_field_errors": [
                    "Каждый вопрос должен быть уникален в списке."
                ],
                "0": {"question": ["Некорректный ID."]},
            },
            response_only=True,
        ),
    ],
    'responses': {
        201: OpenApiResponse(
            description='Ответы успешно созданы или обновлены',
            response=OpenApiTypes.OBJECT,
        ),
    },
}


user_answer_single_create_schema = {
    'summary': 'Ответить на один вопрос',
    'description': (
        'Позволяет авторизованному пользователю ответить на **один вопрос**.\n\n'
        'Если ответ уже существует — он будет обновлён.\n'
        'Если нет — будет создан новый.\n\n'
        'В ответ возвращается автоматически сгенерированный цвет фона '
        'на основе ответов игрока — в формате CSS: `rgb()`, `rgba()` или `linear-gradient()`.\n\n'
        '**Требуется авторизация.**'
    ),
    'examples': [
        OpenApiExample(
            name='Пример запроса',
            summary='Отправка одного ответа',
            description='Передаётся ID вопроса и текст ответа.',
            value={
                "question": 1,
                "answer": "Я родом из далёких гор.",
            },
            request_only=True,
        ),
        OpenApiExample(
            name='Пример успешного ответа',
            summary='Генерация CSS-цвета',
            value={
                "status": "linear-gradient(to right, rgb(34,193,195), rgb(253,187,45))"
            },
            response_only=True,
        ),
        OpenApiExample(
            name='Ошибка валидации',
            summary='Ошибка при неверном ID',
            value={
                "question": ["Некорректный ID."],
            },
            response_only=True,
        ),
    ],
    'responses': {
        200: OpenApiResponse(
            description='Ответ успешно сохранён или обновлён. Возвращён CSS-цвет фона.',
            response=OpenApiTypes.OBJECT,
        ),
    },
}


generate_form_schema = {
    'summary': 'Сгенерировать формы на основе ответа и тела',
    'description': (
        'Позволяет авторизованному пользователю отправить ответ на вопрос, '
        'а также дополнительную информацию (`body`).\n\n'
        'Если ответ на вопрос уже существует — он будет обновлён.\n'
        'Если нет — будет создан новый.\n\n'
        'В ответ возвращаются **сгенерированные формы** (строка или структура), '
        'основанные на истории, ответе и теле запроса.\n\n'
        '**Требуется авторизация.**'
    ),
    'examples': [
        OpenApiExample(
            name='Пример запроса',
            summary='Ответ + тело формы',
            description='Передаётся ID вопроса, ответ и текстовое описание (body), которое влияет на генерацию.',
            value={
                "question": 1,
                "answer": "Мне грустно",
                "body": "JSON",
            },
            request_only=True,
        ),
        OpenApiExample(
            name='Пример успешного ответа',
            summary='Сгенерированная форма',
            value={"forms": "JSON"},
            response_only=True,
        ),
        OpenApiExample(
            name='Ошибка валидации',
            summary='Ошибка при неверных данных',
            value={
                "question": ["Некорректный ID."],
                "body": ["Это поле обязательно."],
            },
            response_only=True,
        ),
    ],
    'responses': {
        200: OpenApiResponse(
            description='Ответ успешно сохранён. Возвращена сгенерированная форма.',
            response=OpenApiTypes.OBJECT,
        ),
    },
}
