# SPDX-FileCopyrightText: 2024-present Dragos Catarahia <dragos@catarahia.me>
#
# SPDX-License-Identifier: MIT

from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI()

    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    return app
