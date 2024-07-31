from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from anyio import to_thread

from fastapi import FastAPI

from .api.main import router as api_router

# AnyIO's default: 40 threads
_ANYIO_DEFAULT_THREAD_LIMIT = 40


def create_app(thread_limit=_ANYIO_DEFAULT_THREAD_LIMIT) -> FastAPI:
    """
    Factory function to create and configure a FastAPI application.

    Whips up a fresh FastAPI instance with a custom thread limit for AnyIO.
    Use this when you want to fine-tune your app's concurrency.

    :param thread_limit: Max number of threads for AnyIO's thread pool.
    :return: A brand new FastAPI application, primed and ready for action.
    """

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        """
        Lifespan context manager for the FastAPI application.

        This function sets the AnyIO thread limit at application startup
        and performs any necessary cleanup when the application shuts down.

        :param app: The FastAPI application instance.
        """
        limiter = to_thread.current_default_thread_limiter()
        limiter.total_tokens = thread_limit
        yield

    app = FastAPI(lifespan=lifespan)

    @app.get('/')
    async def root():
        return {'message': 'Hello World'}

    app.include_router(api_router)

    return app
