
import os
from aiohttp import web
from botbuilder.core import BotFrameworkAdapterSettings, BotFrameworkAdapter
from botbuilder.schema import Activity
from .teams_bot import TeamsRagBot

APP_ID = os.getenv("MICROSOFT_APP_ID","")
APP_PASSWORD = os.getenv("MICROSOFT_APP_PASSWORD","")

adapter_settings = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
adapter = BotFrameworkAdapter(adapter_settings)
bot = TeamsRagBot()

async def messages(req):
    body = await req.json()
    activity = Activity().deserialize(body)
    auth_header = req.headers.get("Authorization","")
    response = await adapter.process_activity(activity, auth_header, bot.on_turn)
    return web.Response(status=201)

app = web.Application()
app.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    web.run_app(app, port=int(os.getenv("PORT","3978")))
