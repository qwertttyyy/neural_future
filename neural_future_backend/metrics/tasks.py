from celery import shared_task

from services.deepseek import generate_rpg_story, generate_rpg_dialog


@shared_task
def generate_story_task(user_id: int, qa_pairs: list[str]):
    """Создание бек-стори героя."""
    return generate_rpg_story(user_id=user_id, user_prompt=qa_pairs)


@shared_task
def generate_dialog_task(user_id: int, npc_id: int, location_id: int):
    """Генерация диалога для второй локации."""
    return generate_rpg_dialog(
        user_id=user_id, npc_id=npc_id, location_id=location_id
    )
