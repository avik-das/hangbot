import asyncio
import os
import sys

import hangups


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


def on_connect_handler(client):
    @asyncio.coroutine
    def on_connect():
        """Handle connecting for the first time."""
        users, convs = \
            yield from hangups.build_user_conversation_list(client)

        convs = reversed(
            sorted(convs.get_all(), key=lambda c: c.last_modified))

        print('USER LIST:')
        print(users)
        print('CONV LIST:')
        print([conversation_name(c) for c in convs])

    return on_connect


if __name__ == '__main__':
    try:
        cookies = get_auth_env()
    except hangups.GoogleAuthError as e:
        sys.exit('Login failed ({})'.format(e))

    client = hangups.Client(cookies)
    client.on_connect.add_observer(on_connect_handler(client))

    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(client.connect())
    finally:
        loop.close()
