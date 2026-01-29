import logging

from notes_app.api.main import APIStateDependency, build_api_app, create_lifespan, run_api
from notes_app.infrastructure.config import load_config
from notes_app.infrastructure.logging.main import setup_logging

logger = logging.getLogger(__name__)


def main() -> None:
    config = load_config()
    setup_logging(config.logging)
    api_dependency = APIStateDependency(config=config)
    lifespan = create_lifespan(api_dependency=api_dependency)
    app = build_api_app(lifespan=lifespan)
    run_api(app=app, api_config=config.api)


if __name__ == "__main__":
    main()
