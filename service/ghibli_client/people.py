from common.client_registry import CachedClient


class PeopleClient(CachedClient):
    name = "people"

    async def get_people(self):
        return await self.get("people", fields="name,films")
