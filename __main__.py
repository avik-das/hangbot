import asyncio
import logging
import logging.handlers
import os
import sys

import hangups

import scripts.swanson


logger = logging.getLogger('hangbot')
logger.setLevel(logging.DEBUG)  # this could depend on the environment

# Terse output, for easy viewing on the console while developing.
stdout_handler = logging.StreamHandler()
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(
    logging.Formatter(
        '%(asctime)s [%(levelname)s] %(message)s',
        '%H:%M:%S'))
logger.addHandler(stdout_handler)

# Verbose output, for debugging after the fact.
file_handler = logging.handlers.RotatingFileHandler(
    'hangbot.log',
    maxBytes=1024 * 1024,
    backupCount=10,
    encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - [%(levelname)s] %(message)s'))
logger.addHandler(file_handler)


ENABLED_SCRIPTS = [
    scripts.swanson,
]


def get_auth_env():
    """
    Wrapper for get_auth that retrieves the credentials from environment
    variables.
    """

    return hangups.auth.get_auth(EnvVarCredentials(), NoCache())


class EnvVarCredentials(object):
    """
    Callbacks for retrieving Google account credentials from environment
    variables.
    """

    @staticmethod
    def get_email():
        """Return Google account email address."""
        return os.environ.get('HANGBOT_EMAIL')

    @staticmethod
    def get_password():
        """Return Google account password."""
        return os.environ.get('HANGBOT_PASSWORD')

    @staticmethod
    def get_verification_code():
        """Return Google account verification code."""

        # Given that the credentials are stored statically in the environment,
        # there's no way to dynamically get the verification code for 2-factor
        # authentication. This means that 2-factor authentication can't be
        # enabled for the bot.
        return None


class NoCache(object):
    """Prevents caching by ignoring attempts to cache the token."""

    def get(self):
        return None

    def set(self, refresh_token):
        return refresh_token


def conversation_name(conv):
    name = conv.name
    if name:
        return name

    users = conv.users
    return ', '.join(u.full_name for u in users)


async def receive_message(message_event, client, conversation):
    """
    For a chat message event, go through the enabled scripts until one of
    them processes a message.
    """

    try:
        for script in ENABLED_SCRIPTS:
            if await script.process(client, conversation, message_event):
                break
    except Exception as e:
        logger.exception('Failed to send process message: %s', e)


def on_event_handler(loop, client, conversation):
    async def on_event(event):
        """Handles the last chat message from the client."""

        if isinstance(event, hangups.ChatMessageEvent):
            if not conversation.get_user(event.user_id).is_self:
                logger.info('Processing message: %s', event.text)
                asyncio.ensure_future(
                    receive_message(
                        event,
                        client,
                        conversation))

    return on_event


def on_connect_handler(loop, client):
    async def on_connect():
        """Handle connecting for the first time."""

        users, convs = await hangups.build_user_conversation_list(client)

        convs = list(reversed(
            sorted(convs.get_all(), key=lambda c: c.last_modified)))

        for conv in convs:
            conv.on_event.add_observer(on_event_handler(loop, client, conv))
            logger.info(
                'Listening to conversation: %s',
                conversation_name(conv))

    return on_connect


if __name__ == '__main__':
    try:
        cookies = get_auth_env()
    except hangups.GoogleAuthError as e:
        sys.exit('Login failed ({})'.format(e))

    try:
        loop = asyncio.get_event_loop()

        client = hangups.Client(cookies)
        client.on_connect.add_observer(on_connect_handler(loop, client))

        loop.run_until_complete(client.connect())
    finally:
        loop.close()
