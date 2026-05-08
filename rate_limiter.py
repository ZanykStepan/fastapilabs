import time
from fastapi import Request, HTTPException
from redis_client import redis_db

RATE_LIMITS = {
    "anonymous": (2, 60),
    "authenticated": (10, 60),
}


async def rate_limit(request: Request, user_id: str | None = None):
    identity = user_id or request.client.host

    limit_type = "authenticated" if user_id else "anonymous"
    limit, period = RATE_LIMITS[limit_type]

    key = f"rate_limit:{limit_type}:{identity}"
    now = int(time.time())
    window_start = now - period

    async with redis_db.pipeline(transaction=True) as pipe:
        pipe.zremrangebyscore(key, min=0, max=window_start)
        pipe.zcard(key)
        pipe.zadd(key, {str(now): now})
        pipe.expire(key, period)

        results = await pipe.execute()

    request_count = results[1]

    if request_count >= limit:
        raise HTTPException(status_code=429, detail="Too many requests")