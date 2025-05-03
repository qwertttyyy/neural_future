from typing import List

from django.conf import settings
from django.contrib.auth import get_user_model
from openai import OpenAI

User = get_user_model()

client = OpenAI(
    api_key=settings.DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com",
)

DEFAULT_SYSTEM_PROMPT = """
You are a fantasy RPG storyteller. Based on the player's answers to NPC questions,
create a vivid 150-200-word back-story in second person (“You …”), heroic tone.
Use the answers logically, do not list the questions, output only the story.
Answer in Russian.
"""


def generate_rpg_story(
    user_id: int,
    user_prompt: List[str],
    system_prompt: str | None = None,
) -> str:
    """
    :param user_id: id игрока
    :param user_prompt: список строк вида ["Q: …", "A: …", ...]
    :param system_prompt: кастомный system prompt
    :return: сгенерированная история
    """
    sys_prompt = system_prompt or DEFAULT_SYSTEM_PROMPT

    messages = [
        {"role": "system", "content": sys_prompt},
        {
            "role": "user",
            "content": "\n".join(user_prompt),
        },
    ]

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        temperature=0.9,
        max_tokens=300,
    )

    story = response.choices[0].message.content.strip()

    user = User.objects.get(pk=user_id)
    user.story = story
    user.save()

    return story
