from asyncio import gather
from sanic.views import HTTPMethodView
from sanic.response import json
from service.ghibli_client import ClientRegistry
from service.domain.movies import get_movies


class MoviesResource(HTTPMethodView):
    async def get(self, request):
        films, people = await gather(
            ClientRegistry.get_cached("films").get_films(),
            ClientRegistry.get_cached("people").get_people()
        )
        return json(get_movies(films, people))

