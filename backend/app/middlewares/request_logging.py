import logging
import time
import uuid

from fastapi import Request

logger = logging.getLogger("uvicorn.access")


async def request_logging_middleware(request: Request, call_next):
    # 为每个请求生成 request_id，便于串联排障
    request_id = str(uuid.uuid4())
    start = time.perf_counter()

    response = await call_next(request)

    # 计算耗时（毫秒）并输出结构化日志到 stdout
    duration_ms = round((time.perf_counter() - start) * 1000, 2)
    logger.info(
        "request_id=%s method=%s path=%s status=%s duration_ms=%s",
        request_id,
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    response.headers["X-Request-ID"] = request_id
    return response
