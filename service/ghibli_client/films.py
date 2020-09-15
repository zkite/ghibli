from common.client_registry import CachedClient


class FilmsClient(CachedClient):
    name = "films"

    async def get_films(self):
        return await self.get("films", fields="title,id")
