from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI


def set_up_cors(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True
    )
