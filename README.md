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

python .

# Press ^C to exit
```

Currently, all this will do is list your conversations, most recently modified first.

Limitations
-----------

This project builds heavily off the excellent [hangups](https://github.com/tdryer/hangups) library. As the README for that libary explains, Google Hangouts uses a proprietary protocol, so any communication with Google Hangouts has been reversed engineered.

Contributing
------------

Before contributing a change, please run the following checks:

```sh
# The first time, install the flake8 git commit hook. Only needs to be done
# once.
flake8 --install-hook=git

# There are no automated tests yet. Once they are set up, instructions will be
# added on how to run them.
```
