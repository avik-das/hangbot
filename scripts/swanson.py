"""
Respond to:

    hangbot swanson me

with a random quote from Ron Swanson of Parks & Recs.
"""

import asyncio
import hangups
import logging
import requests


logger = logging.getLogger('hangbot.scripts.swanson')


API_URL = 'http://ron-swanson-quotes.herokuapp.com/v2/quotes'
COMMAND = 'hangbot swanson me'


async def process_message(client, conversation, message_event):
    if message_event.text and \
            message_event.text.strip().lower() == COMMAND:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, requests.get, API_URL)
        quote = response.json()[0]

        segments = hangups.ChatMessageSegment.from_str(
            '"{}"\n- Ron Swanson'.format(quote))
        await conversation.send_message(segments)

        return True

    return False
