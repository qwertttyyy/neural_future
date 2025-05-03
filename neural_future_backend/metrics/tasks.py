from celery import shared_task

from services.deepseek import generate_rpg_story


@shared_task
def generate_story_task(user_id: int, q_a_pairs: list[str]):
    """
    Вызывается асинхронно. q_a_pairs — список строк ["Q: …", "A: …", …]
    """
    return generate_rpg_story(user_id, q_a_pairs)
