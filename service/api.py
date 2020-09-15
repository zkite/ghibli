from sanic import Blueprint
from sanic.app import Sanic


def load_api(app: Sanic):
    from service.resources.movies import MoviesResource

    api_prefix = f"/{app.config.get('SERVICE_NAME')}/v1"
    api = Blueprint("v1", url_prefix=api_prefix, strict_slashes=False)

    # get the endpoints here
    api.add_route(MoviesResource.as_view(), "/movies", strict_slashes=False)

    app.blueprint(api)
