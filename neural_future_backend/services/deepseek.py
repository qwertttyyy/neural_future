import json
import re
from typing import List, Dict, Any

from django.conf import settings
from django.db import transaction
from openai import OpenAI
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from metrics.models import UserAnswer, SystemPromt
from npc.models import NPC, Location, Question, AnswerVariant
from users.models import CustomUser as User

client = OpenAI(
    api_key=settings.DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com",
)


# ─────────────────────────── helpers ────────────────────────────
def _deepseek_chat(
    system_promt, user_promt, json_output=False, *, max_tokens: int = 400
) -> str:
    messages = [
        {"role": "system", "content": system_promt},
        {"role": "user", "content": user_promt},
    ]
    params = {
        'model': "deepseek-chat",
        'messages': messages,
        'temperature': 0.9,
        'max_tokens': max_tokens,
    }
    if json_output:
        params['response_format'] = {'type': 'json_object'}

    """Единая точка обращения к DeepSeek."""
    resp = client.chat.completions.create(
        **params,
    )
    return resp.choices[0].message.content.strip()


def get_system_promt(promt_name) -> SystemPromt:
    try:
        return SystemPromt.objects.get(name=promt_name)
    except SystemPromt.DoesNotExist:
        raise serializers.ValidationError(
            {'detail': f'Необходимо создать промт с именем {promt_name}'}
        )


COLOR_SYSTEM_PROMPT = """
Ты — нейросеть, которая помогает человеку пройти психологический тест «Дом страхов».
Суть теста: человек представляет Дом, в котором никогда бы не захотел жить. Через его ответы мы выявляем глубинные страхи и тревоги человека.
На основе уже данных ответов внимательно проанализируй текущие эмоции, страхи и психологическое состояние человека.
Теперь выбери и верни одно единственное значение, которое наиболее точно отразит эмоциональное состояние человека после его последнего ответа. Это значение должно быть строкой для использования в CSS-свойстве background-color.
Правила для генерации значения:
Формат: rgb(), rgba() или linear-gradient()
Выбирай цвета осмысленно, исходя из текущего психологического состояния, отраженного в ответах:
Темные, мрачные, холодные оттенки для глубокого страха, тревоги или негативных эмоций.
Смешанные или переходные градиенты для неопределённости или смешанных чувств.
Более светлые или теплые оттенки, если страхи поверхностны или слабо выражены.
Верни только строку CSS-свойства background-color без дополнительного текста и комментариев.
"""


def get_prev_answers(user_id, question_id, answer):
    q = get_object_or_404(Question, pk=question_id)
    prev_qs = list(
        Question.objects.filter(
            npc=q.npc, location=q.location, id__lt=q.id
        ).order_by("id")
    )
    ua_map = {
        ua.question_id: ua.answer
        for ua in UserAnswer.objects.filter(
            user_id=user_id, question__in=prev_qs
        )
    }
    lines = [
        f"{question.question}: {ua_map[question.id]}"
        for question in prev_qs
        if question.id in ua_map
    ]
    lines.append(f"{q.question}: {answer}")
    return "\n".join(lines)


def generate_background_color(
    user_id: int, question_id: int, answer: str
) -> str:
    """
    Формирует системный prompt, собирая все предыдущие пары «вопрос: ответ»
    для того же NPC и локации, и добавляя текущую пару.
    Возвращает готовую строку с подстановкой в DEFAULT_SYSTEM_PROMPT.
    """
    pairs = get_prev_answers(user_id, question_id, answer)

    color_system_promt = get_system_promt("color")
    return _deepseek_chat(
        color_system_promt.text,
        pairs,
        max_tokens=color_system_promt.max_tokens,
    )


def generate_forms(user_id: int, question_id: int, answer: str, body: str):
    pairs = get_prev_answers(user_id, question_id, answer)
    forms_system_promt = get_system_promt('forms')
    system_promt = f'{forms_system_promt.text}\n{pairs}'
    return _deepseek_chat(
        system_promt, body, max_tokens=forms_system_promt.max_tokens
    )


def _strip_code_block(s: str) -> str:
    """
    Убирает markdown-фехинг ```...``` вокруг JSON.
    """
    pattern = r"```(?:json)?\s*\n([\s\S]+?)\n```"
    m = re.search(pattern, s)
    return m.group(1) if m else s


# ─────────────────────── генерация истории ──────────────────────
STORY_SYSTEM_PROMPT = """
You are a fantasy RPG storyteller. Based on the player's answers to NPC questions,
create a vivid 150-200-word back-story in second person (“You …”), heroic tone.
Use the answers logically, do not list the questions, output only the story.
Answer in Russian.
"""


def generate_rpg_story(user_id: int, user_prompt: List[str]) -> str:
    messages = [
        {"role": "system", "content": STORY_SYSTEM_PROMPT},
        {"role": "user", "content": "\n".join(user_prompt)},
    ]
    story = _deepseek_chat(
        messages,
        '',
        max_tokens=300,
    )

    user = User.objects.get(pk=user_id)
    user.story = story
    user.save(update_fields=["story"])
    return story


# ───────────── генерация диалога для второй локации ─────────────
DIALOG_SYSTEM_PROMPT = """
Ты сценарист фэнтези-RPG. Получаешь историю героя и имя NPC.
Нужно создать компактный JSON-объект **в одну строку** (минимизированный, без пробелов и переводов строк,
кроме пробелов внутри самих строк).

Формат:

{"npc":"<имя NPC>","dialog":[{"question":"<вопрос>","answers":["<реплика игрока 1>","<реплика игрока 2>",…]} …]}

Правила:
• Вопросы задаёт NPC (от третьего лица).
• Каждый элемент массива answers — это возможная реплика игрока (от первого лица).
• 1-5 вопросов; у каждого 1-4 вариантов ответа.
• Русский язык, стиль фэнтези-RPG.
• Верни **только** JSON в одну строку, без markdown-блоков и комментариев.
"""


def generate_rpg_dialog(
    user_id: int, npc_id: int, location_id: int
) -> Dict[str, Any]:
    user = User.objects.get(pk=user_id)
    npc = NPC.objects.get(pk=npc_id)
    location = Location.objects.get(pk=location_id)

    messages = [
        {"role": "system", "content": DIALOG_SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"История героя:\n{user.story}\nNPC: {npc.name}",
        },
    ]

    raw = _deepseek_chat(messages, '', json_output=True, max_tokens=500)
    print(raw)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        cleaned = _strip_code_block(raw)
        data = json.loads(cleaned)

    with transaction.atomic():
        for item in data.get("dialog", []):
            q = Question.objects.create(
                npc=npc, location=location, question=item["question"]
            )
            variants = [
                AnswerVariant(question=q, variant=ans)
                for ans in item.get("answers", [])[:4]
            ]
            AnswerVariant.objects.bulk_create(variants)

    return data
