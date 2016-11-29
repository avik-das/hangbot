"""
Respond to:

    hangbot swanson me

with a random quote from Ron Swanson of Parks & Recs.
"""

import asyncio
import hangups
import logging
import re
import requests


logger = logging.getLogger('hangbot.scripts.swanson')


API_URL = 'http://ron-swanson-quotes.herokuapp.com/v2/quotes'
MESSAGE_REGEX = re.compile(r'^hangbot swanson me$', re.IGNORECASE)


async def process(client, conversation, message_event):
    if MESSAGE_REGEX.match(message_event.text):
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, requests.get, API_URL)
        quote = response.json()[0]

        segments = hangups.ChatMessageSegment.from_str(
            '"{}"\n- Ron Swanson'.format(quote))
        conversation.send_message(segments)
        await conversation.send_message(segments)

        return True

    return False
