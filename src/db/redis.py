# inside src/db/redis.py

import aioredis
from src.config import config

redis = None
JTI_EXPIRY = 3600


token_blocklist = aioredis.from_url(config.REDIS_URL)

# создаем подключение
async def get_redis():
    global redis
    if redis is None:
        redis = await aioredis.from_url(
            f"redis://:{config.REDIS_PASSWORD}@{config.REDIS_HOST}:{config.REDIS_PORT}/0",
            decode_responses=True
        )
    return redis


# добавляем JTI в блоклист
async def add_jti_to_blocklist(jti: str) -> None:
    r = await get_redis()
    await r.set(name=jti, value="", ex=JTI_EXPIRY)

# проверяем, есть ли JTI в блоклисте
async def token_in_blocklist(jti: str) -> bool:
    r = await get_redis()
    return await r.exists(jti) == 1