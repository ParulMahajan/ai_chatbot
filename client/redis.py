import os
import json
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from util_ai.logger import logger  as log

host = os.getenv("REDIS_HOST")
port = os.getenv("REDIS_PORT", 6379)  # Default Redis port is 6379
password = os.getenv("REDIS_PASSWORD", None)  # Optional password

class CustomRedisChatMessageHistory(RedisChatMessageHistory):
    def add_message(self, message: BaseMessage) -> None:
        # Store only the message content
        content = {
            "type": message.type,
            "data": {
                "content": message.content}
        }
        self.redis_client.rpush(self.key, json.dumps(content))

    @property
    def messages(self):
        # Retrieve messages in reverse order (newest first)
        items = [json.loads(m) for m in self.redis_client.lrange(self.key, 0, -1)]
        messages = []
        for item in items:
            log.debug(f"message item: {item}")
            if item["type"] == "human":
                messages.append(HumanMessage(content=item["data"]["content"]))
            elif item["type"] == "ai":
                messages.append(AIMessage(content=item["data"]["content"]))
        return messages

# Construct URL with password if it exists
redis_url = (
    f"redis://:{password}@{host}:{port}"
    if password
    else f"redis://{host}:{port}"
)

def get_history(session_id: str):
    return CustomRedisChatMessageHistory(
        session_id=session_id,
        url=redis_url,
        key_prefix="user:")


