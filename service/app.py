from sanic.app import Sanic
from service import api
from config import Config
from common.cache_manager import RedisCacheManager
from common.client_registry import ClientRegistry
from common.constants import DEFAULT_SERVICE_NAME


app = Sanic(DEFAULT_SERVICE_NAME)
app.config.from_object(Config)


api.load_api(app)


@app.listener("before_server_start")
async def before_server_start(app, loop):
    ClientRegistry.init(RedisCacheManager)


@app.listener("after_server_stop")
async def after_server_stop(app, loop):
    await RedisCacheManager.close()
