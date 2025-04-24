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
                    "id": 10,
                    "user": "mikhail",
                    "question": "Как тебя зовут?",
                    "answer": "Меня зовут Михаил",
                },
                {
                    "id": 11,
                    "user": "mikhail",
                    "question": "Сколько тебе лет?",
                    "answer": "25",
                },
                {
                    "id": 12,
                    "user": "mikhail",
                    "question": "Откуда ты?",
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
