from urllib.parse import parse_qs
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token
from channels.db import database_sync_to_async


class TokenAuthMiddleware:
    """Прокладываем токен ?token=<key>"""

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        scope['user'] = AnonymousUser()

        qs = parse_qs(scope.get('query_string', b'').decode())
        token_key = qs.get('token', [None])[0]

        if token_key:
            user = await self.get_user(token_key)
            if user:
                scope['user'] = user

        return await self.inner(scope, receive, send)

    @database_sync_to_async
    def get_user(self, key):
        try:
            return Token.objects.select_related('user').get(key=key).user
        except Token.DoesNotExist:
            return None
