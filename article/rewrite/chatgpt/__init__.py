import aiohttp
from django.conf import settings

from .exceptions import ChatGptClientError


async def send_request_to_chatgpt(prompt, api_key):
    if not settings.CHATGPT_API_KEY:
        raise ChatGptClientError('CHATGPT_API_KEY missing in settings')
    
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.CHATGPT_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",  # Replace with the desired model
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 150
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            response_json = await response.json()
            return response_json