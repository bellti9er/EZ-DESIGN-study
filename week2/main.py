import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from wiki_api import WikiSearchAPI
from decorators import log_request_handler, cache_response, exception_handler

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI()


@app.get("/")
@log_request_handler
@cache_response
@exception_handler
async def process_request(request: Request, query: str = None) -> JSONResponse:
    wiki_api = WikiSearchAPI()
    search_result = await wiki_api.search(query)

    return JSONResponse(status_code=200, content=search_result)


@app.get("/error/")
@log_request_handler
@cache_response
@exception_handler
async def process_error_request(request: Request, query: str = None) -> JSONResponse:
    message = request.query_params.get("message")

    raise Exception(message)
