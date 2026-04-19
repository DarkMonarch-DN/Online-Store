import time

from fastapi import Request, Response
from loguru import logger


async def log_requests(request: Request, call_next):
    start_time = time.time()

    logger.info(f"Incoming request: {request.method} {request.url.path}")

    response: Response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = f"{process_time:.2f}ms"

    log_message = f"Completed: {request.method} { request.url.path} | Status: {response.status_code} | Duration: {formatted_process_time}"

    if response.status_code >= 400:
        logger.error(log_message)
    else:
        logger.success(log_message)

    return response