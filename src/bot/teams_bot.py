
import os, aiohttp
from botbuilder.core import ActivityHandler, TurnContext

RAG_API = os.getenv("RAG_API_URL", "http://localhost:8000/api/chat")

class TeamsRagBot(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        user_text = turn_context.activity.text or ""
        async with aiohttp.ClientSession() as s:
            async with s.post(RAG_API, json={"question": user_text}, timeout=60) as r:
                r.raise_for_status()
                data = await r.json()
        await turn_context.send_activity(data["answer"])

    async def on_members_added_activity(self, members_added, turn_context: TurnContext):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hi! I’m your Policy Bot. Ask me anything about our procedures.")
