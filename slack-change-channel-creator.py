#! /usr/bin/env python3
import sys
from slacker import Slacker, Error

# Get channel names from command line
try:
    channel_name = sys.argv[1].strip('\'"')
    copy_channel_name = sys.argv[2].strip('\'"')
    assert channel_name
    assert copy_channel_name
except:
    print("Usage: python slack-change-channel-creator.py new_channel channel_to_copy_users_from")
    sys.exit(1)

# Load API key from apikey.txt
try:
    with open('apikey.txt') as f:
        api_key = f.read().strip()
        assert api_key
except IOError:
    print("Cannot find apikey.txt, or other reading error")
    sys.exit(1)
except AssertionError:
    print("Empty API key")
    sys.exit(1)
else:
    slack = Slacker(api_key)


# Load blacklist
try:
    with open('blacklist.txt') as f:
        blacklist = f.readlines()
	assert blacklist
except IOError:
    print("Cannot find blacklist.txt, or other reading error. Ignoring.")
except AssertionError:
    print("Empty or broken blacklist. Ignoring.")
else:
    backlist = [x.strip() for x in blacklist]   # Remove Whitespace Characters
    # Get User IDs from names
    response = slack.users.list()
    blacklist = [d for d in response.body['members'] if d['name']+"\n" in blacklist]
    blacklist = [row['id'] for row in blacklist]


# Create channel and get id from name
response = slack.channels.list()
channels = [d for d in response.body['channels'] if d['name'] == channel_name.lower()]
if not len(channels):
    print("Cannot find channel. Create it...")
    slack.channels.create(channel_name)
    response = slack.channels.list()
    channels = [d for d in response.body['channels'] if d['name'] == channel_name.lower()]
assert len(channels) == 1
channel_id = channels[0]['id']



# Get copy-channel id from name
response = slack.channels.list()
channels = [d for d in response.body['channels'] if d['name'] == copy_channel_name.lower()]
if not len(channels):
    print("Cannot find channel")
    sys.exit(1)
assert len(channels) == 1
copy_channel_id = channels[0]['id']

# Get users list from copy-channel
response = slack.channels.info(copy_channel_id)
users = response.body['channel']['members']

# Delete all Users who are in the blacklist from the array
users = [x for x in users if x not in blacklist]

# Invite all users to slack channel
for id in users:
    print("Inviting {} to {}".format(id, channel_name))
    try:
        slack.channels.invite(channel_id, id)
    except Error as e:
        code = e.args[0]
        if code == "already_in_channel":
            print("{} is already in the channel".format(id))
        elif code == 'cant_invite_self':
            slack.channels.join(channel_name)
        elif code in ('cant_invite', 'user_is_ultra_restricted'):
            print("Skipping user {} ('{}')".format(id, code))
        else:
            raise

print('done')
