# -*- coding: utf-8 -*-
# @Date    : 2018-12-07 13:42:51
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
import base64
from django.conf import settings
from itsdangerous import URLSafeTimedSerializer as USTS


class TokenGenerator:

    def __init__(self, secret_key):
        self.secret_key = secret_key
        self.salt = base64.encodebytes(secret_key.encode())

    def make_token(self, _id):
        serializer = USTS(self.secret_key)
        return serializer.dumps(_id, self.salt)

    def check_token(self, token, expiration=3600):
        serializer = USTS(self.secret_key)
        return serializer.loads(token, salt=self.salt, max_age=expiration)

    def remove_token(self, token):
        serializer = USTS(self.secret_key)
        return serializer.loads(token, salt=self.salt)


token_generator = TokenGenerator(settings.SECRET_KEY)
