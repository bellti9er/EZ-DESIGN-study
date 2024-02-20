from typing import Callable

import time
import json
import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from cache_storage import CacheStorage


def log_request_handler(func: Callable) -> Callable:
    async def wrapper(request: Request, query: str = None) -> JSONResponse:
        start_time: float = time.time()
        response: JSONResponse = await func(request, query)
        process_time: float = time.time() - start_time
        client_ip: str = request.client.host if request.client else None

        log_message = json.dumps(
            {
                "request_process_time": process_time,
                "request_method": request.method,
                "request_url": str(request.url),
                "client_ip": client_ip,
                "response_status_code": response.status_code,
            }
        )
        logging.info(log_message)

        return response

    return wrapper


def cache_response(func: Callable) -> Callable:
    async def wrapper(request: Request, query: str = None) -> JSONResponse:
        cache: CacheStorage = CacheStorage()
        cache_key: str = f"{request.url}-{request.method}-{request.client.host}-{request.query_params}"
        cached_response: JSONResponse = cache.get(cache_key)

        if cached_response:
            return JSONResponse(status_code=200, content=json.loads(cached_response))

        response: JSONResponse = await func(request, query)
        cache.set(cache_key, response.body.decode("utf-8"))

        return response

    return wrapper


def exception_handler(func: Callable) -> Callable:
    async def wrapper(request: Request, query: str = None) -> JSONResponse:
        try:
            return await func(request, query)
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": str(e)})

    return wrapper
