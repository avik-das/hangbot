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


def send_message_callback(event, client, conversation):
    def send_message():
        """
        For a chat message event, send a response reflecting the same message.
        """

        segments = hangups.ChatMessageSegment.from_str(
            '[FROM HANGBOT] {}'.format(event.text))
        conversation.send_message(segments)
        (asyncio.async(conversation.send_message(segments))
            .add_done_callback(on_message_sent))

    def on_message_sent(future):
        """Handle showing an error if a message fails to send."""

        try:
            future.result()

            print()
        except hangups.NetworkError:
            print('Failed to send message')

    return send_message


def on_event_handler(loop, client, conversation):
    def on_event(event):
        """Handles the last chat message from the client."""

        if isinstance(event, hangups.ChatMessageEvent):
            loop.call_soon(show_event(event))
            if not conversation.get_user(event.user_id).is_self:
                loop.call_soon(
                    send_message_callback(
                        event,
                        client,
                        conversation))

    def show_event(event):
        def print_event():
            print(event.text)
        return print_event

    return on_event


def on_connect_handler(loop, client):
    @asyncio.coroutine
    def on_connect():
        """Handle connecting for the first time."""

        users, convs = \
            yield from hangups.build_user_conversation_list(client)

        convs = list(reversed(
            sorted(convs.get_all(), key=lambda c: c.last_modified)))

        print('Conversations:')
        for i, c in enumerate(convs):
            c.on_event.add_observer(on_event_handler(loop, client, c))
            print('  {:>3}. {}'.format(i, conversation_name(c)))
        print()

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
