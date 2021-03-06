"""
Respond to:

    /giphy [tag]

with a random image from Giphy (optionally limited by tag)
"""

import asyncio
import functools
import hangups
import logging
import requests


logger = logging.getLogger('hangbot.scripts.giphy')


API_KEY = 'dc6zaTOxFJmzC'  # Use the public API key for now
API_URL = 'http://api.giphy.com/v1/gifs/random'
COMMAND = '/giphy'


async def process_message(client, conversation, message_event):
    if message_event.text and message_event.text.startswith(COMMAND):

        params = {
            'api_key': API_KEY,
            'tag': message_event.text[len(COMMAND):].strip()
        }

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, functools.partial(requests.get, API_URL, params=params))
        response_json = response.json()

        image_name = '{}.gif'.format(response_json['data']['id'])
        image_url = response_json['data']['image_url']

        # Download the image file directly into memory
        image_file = await loop.run_in_executor(
            None, functools.partial(requests.get, image_url, stream=True))
        image_id = await client.upload_image(
            image_file=image_file.raw, filename=image_name)

        # Send an empty message; we only want to show the image
        segments = hangups.ChatMessageSegment.from_str('')
        await conversation.send_message(segments, image_id=image_id)

        return True

    return False
