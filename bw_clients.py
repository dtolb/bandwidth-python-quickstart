import os
from bandwidth import messaging, voice, account

# Grab environment variables.
user_id = os.environ.get('BANDWIDTH_USER_ID')
token = os.environ.get('BANDWIDTH_API_TOKEN')
secret = os.environ.get('BANDWIDTH_API_SECRET')

# Make sure the evn variables are set
if not all((user_id, token, secret)):
    print('Please make sure you have set your user_id, token, and secret as environment variables')
    sys.exit();

# Works best if you include each of these individually
messaging_api = messaging.Client(user_id, token, secret)
voice_api = voice.Client(user_id, token, secret)
account_api = account.Client(user_id, token, secret)

app_name = 'bandwidth-python-quickstart'

call_path = '/inbound-voice-callbacks'
message_path = '/inbound-message-callbacks'