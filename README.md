Hangbot
=======

A bot for Google Hangouts, developed for personal needs. The goal is not to have a bot that fits everyone's needs, but to learn more about Google Hangouts, as well as developing bots.

Quick Start
-----------

```sh
git clone https://github.com/avik-das/hangbot.git
cd hangbot

# Set up your virtualenv if you wish
#
#   pyenv install 3.5.2
#   pyenv virtualenv 3.5.2 hangbot
#   pyenv local hangbot
#   echo '.python-version' >> .git/info/exclude

# Or otherwise sure you're using Python 3.5

pip install -r requirements.txt

export HANGBOT_EMAIL='...'
export HANGBOT_PASSWORD='...'

# Make sure you have some hangouts conversations with the above user as a
# member, as those are the conversations the bot will listen to.

python .

# Press ^C to exit
```

Now you can send commands to the bot. See the `scripts` directory for available commands.

Limitations
-----------

This project builds heavily off the excellent [hangups](https://github.com/tdryer/hangups) library. As the README for that library explains, Google Hangouts uses a proprietary protocol, so any communication with Google Hangouts has been reversed engineered.

Contributing
------------

Before contributing a change, please run the following checks:

```sh
# The first time, install the flake8 git commit hook. Only needs to be done
# once.
flake8 --install-hook=git

# The above will automatically run the linter whenever you commit, but it's a
# good habit to just run it across the whole project occasionally.
flake8

# There are no automated tests yet. Once they are set up, instructions will be
# added on how to run them.
```

Running as a Daemon
-------------------

In production, we want to run the bot as a daemon, as well as automatically restart it if it crashes. This project uses [the `forever` tool](https://github.com/foreverjs/forever) to achieve this. To run the bot in production:

```sh
# Make sure you have node.js installed. Any version that forever.js supports is
# sufficient.

npm install

# Start the daemon
npm start

# Now you can directly use "forever" to monitor and interact with the running
# process. Because the tool isn't installed globally, you'll have to point to
# the correct executable. Examples include:
./node_modules/.bin/forever          # see all the available options
./node_modules/.bin/forever list     # see all running daemons
./node_modules/.bin/forever logs .   # see the latest STDOUT output for the bot
./node_modules/.bin/forever stop .   # stop the bot
```
