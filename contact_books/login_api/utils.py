import traceback
import uuid
from datetime import datetime
import jwt
import logging
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from helpers.my_sql_connector import my_sql_execute_query

PRIVATE_KEY = """
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCu+3hU65jUp2qi
+fRJDmjm2hUcNaq6FUH+QqhX/kZ8DXxAaorqs0BHzbpGUyizM01hxB5DeolbfBoB
ZWTnGw6UZqo1JUpxJKfqRy4zh8i3kfr3WnOHan2fJPtF470MihDgA1PgGK1IAddZ
25XIX1lmMRvTdWbUP0KsSz6dIeV7Al5CKAsD5sUI749k/J+6hROe8tDZGsliSt1N
8LVUqPwarfBhbnPYX5AetFspUB7hopjwDlhgL79ttSBtqpLYkSUqHteIe5t4yWld
402sYhCWtOO3PeqLlarzRBvfDr6tij/wUVlxFip/ZWBwVZN7c4KIeER3al64YOpb
i8A7TYW3AgMBAAECggEADqZxQbLj/dHyhKimwkMZl1Jk+BKqM6A6AT61d4CLiDFc
2MvSy6msVRatZNvriW1fKjNQUVf+DhHK35kMpKjIRLZ/w6lWnThzcpL5FElnDa+E
Mpd5GrpYwC1JeGWD23vnw8mjiRynzWKSFCzlUnxhMMQlz0OCE30kaOZ33JIM84pw
qWcrkZpKnhvwSD/Q3GVd9VcO+FvotKztsUQLv6BCvphq1LjAtlzC+tSESJTHmhkm
5ixXxdbtwCvrmE3uxXX1n0FqKMpT1UfAwBcNjwQf3B0A9BUALRyuNl6Fv10KUkCj
yXXdurpv+o/uXWMiZx/X9SRpOF6Yj454AJoNsnoY2QKBgQDldmhOcajaSP+G4GKj
zcJd1WTcOA8zi0/Jgt3866BeyjRVZTZa1AqakfWa8505uNvxC3ZOO6V03d0sLXCa
u/lq7NAk0ZSLgsap5h+nErDcjMonLbws3uRfomRd5tpo6A/XJqhiV9nzy40T6eoF
BUVz5ghKD84nNY/GdRc/UKBYxQKBgQDDOBdnb2WEdjIUXBmJJFEiLqgdbvFQqzAn
hQIoKoO4wTAOW74qgegwTvMj0K+q2GZP1qHu4ySN4aV7xnoeBkHUlwZQ0jharNPD
oKTT5lzDHusbSnofvVr3SV/yUpYj4fyTtNIzNcfeMlUzISdm+pPPOuQiTjzy93R0
tGQRGtW0SwKBgCR6zZxi/3gskMstkyD9jkACs/U6yFfmdvnPX2FdSHKpbOaCn8CS
41iticFnp4BMvlK1AsrvOp+4wffLBZLj/YQdP/4Kf7YqRVEvb6rNEucNTvopkDgF
+4Kku5YeJGz3L8WBtNVlqBXVL4mR7416yA7j7D9yAdFD96aSaO6877ENAoGAYIMK
jwhzl9kXSRl/Rl29/rgyRNrkUo1PcTpAprreBCj+KRsSGNHAiKF/cuVo832oly/1
PrTtDXfQ6DBnjxBo20EOzkYftjRbPQvecSQiGBThBsz7M1XZ8wdDd/l8YKEIzb1H
binYdfFMTcrGQBMBoCHtR0iGuVe9KzVDg3FQ1aECgYAF/5JQq9V2bPzauGqdMKIS
ce1JqVkuw8dansid7XejdVwH6QmgMrkt4elk5zV74vqOJs0D057cwVvW7bPj6dd6
DLSj0gTEvd97D8X8xMc/CeIifO8M16SwuoqDf5xdtOVDjnFFvc1y+25Pl9Z2Xkud
w3O4APa3T59+oY5XeyqfSg==
"""


def generate_bearer_token(email):
    response = {"status": "Internal Server Error", "status_code": 500, "message": "Error in Generating Bearer Token"}
    try:
        query = f"select * from auth_user where email = '{email}'"
        results, status_code = my_sql_execute_query(query)
        if status_code == 500:
            return response
        user_id = results[0][0]
        email = results[0][1]
        x_api_key = results[0][5]
        jti = str(uuid.uuid4())  # generating unique JSON token id for more security
        date = datetime.now()
        current_timestamp = date.timestamp()
        payload = {
            "exp": current_timestamp + 86400,  # 30 mins expiry set
            "generated_at": current_timestamp,
            "jti": jti,
            "user_id": f"{user_id}",
            "email": f"{email}",
            "x_api_key": f"{x_api_key}"
        }

        token = jwt.encode(payload, PRIVATE_KEY, algorithm="HS256")
        if isinstance(token, bytes):
            token = token.decode('utf-8')
        response.update(
            {
                "status": "success",
                "token": token,
                "xapi": x_api_key,
                "status_code": 200,
                "message": "Bearer Token Generated Successfully"
            }
        )

    except Exception as e:
        logging.info(e)
        traceback.print_exc()
    return response


def generate_private_key():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    return pem.decode('utf-8')

