# fastapi
from fastapi import FastAPI

from app.core.modules import init_routers, make_middleware
from app.core.settings import config
from app.seeders.database_seeder import DatabaseSeeder


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="SurveilSync Backend API",
        description="Backend API for the SurveilSync project.",
        version="1.0.0",
        # docs_url=None if config.ENVIRONMENT == "production" else "/docs",
        # redoc_url=None if config.ENVIRONMENT == "production" else "/redoc",
        middleware=make_middleware(),
    )
    init_routers(app_=app_)
    # init_listeners(app_=app_)
    # init_cache()

    # Run database seeders
    DatabaseSeeder.run()

    return app_


app = create_app()
