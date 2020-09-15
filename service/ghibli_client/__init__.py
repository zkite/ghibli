from common.client_registry import ClientRegistry
from service.ghibli_client.films import FilmsClient
from service.ghibli_client.people import PeopleClient

__all__ = ("ClientRegistry",)

ClientRegistry.register("films", FilmsClient)
ClientRegistry.register("people", PeopleClient)
