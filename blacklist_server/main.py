import logging.config

from fastapi import FastAPI

from config.logging import logging_config
from .contracts import CheckResponse, CheckRequest

app = FastAPI()

logging.config.dictConfig(logging_config)

black_list = [
    'Leslie White',
    'Ilya Lystsov',
    'Peter Griffin',
    'Paul Anderson',
]


@app.post("/check", response_model=CheckResponse)
async def is_in_list(request: CheckRequest) -> CheckResponse:
    in_list = request.name in black_list
    return CheckResponse(in_list=in_list)
