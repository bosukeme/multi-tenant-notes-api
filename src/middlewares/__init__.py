from fastapi import FastAPI
from src.middlewares.logging import set_up_logging
from src.middlewares.rate_limit import set_up_limiter
from src.middlewares.cors import set_up_cors
from src.middlewares.errors import set_up_error_handlers


def register_middleware(app: FastAPI):
    set_up_error_handlers(app)
    set_up_limiter(app)
    set_up_cors(app)
    set_up_logging(app)
