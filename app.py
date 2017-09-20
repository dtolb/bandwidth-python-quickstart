import os
import sys
import pprint
import json

from bandwidth import messaging, voice, account
from flask import Flask, request

app = Flask(__name__)

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

def po(o):
    """
    Prints things to console much more nicely than the default print
    """
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(o)

# Just a nice hello world :)
@app.route('/')
def hello():
    return 'Hello World From Bandwidth!!'

@app.route('/inbound-voice-callbacks', methods=['POST'])
def handle_voice():
    """
    Setup a callback handler for POST voice events, with AUTO-ANSWER
    keep in mind that if you have this setup in a BXML (for voice) app you will
    need to rework the response. And change the method to GET
    """
    callback_event = request.get_json()
    po(callback_event)

    # Get the event type
    event_type = callback_event['eventType']

    # get the call id
    call_id = callback_event['callId']

    # ignore incoming call events
    if event_type == 'incomingCall':
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    # here we go, call is answered
    elif event_type == 'answer':

        # Play mp3
        voice_api.play_audio_to_call(call_id, 'https://s3.amazonaws.com/bwdemos/hello.mp3')
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    # Finally if the playback is over hangup the call
    elif event_type == 'playback' and callback_event['status'] == 'done':
        voice_api.hangup_call(call_id)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    elif event_type == 'hangup':

        #send a message to them 
        messaging_api.send_message( from_ = callback_event['to'],
                                  to = callback_event['from'],
                                  text = ':) That was fun!',
                                  media = ['https://s3.amazonaws.com/bwdemos/hello.jpg'])
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    else:
        # Ignore everything else
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/inbound-message-callbacks', methods=['POST'])
def handle_message():
    """
    Setup a callback handler for POST message events, keep in mind that if you
    have this setup in a BXML (for voice) app, that this should be GET as well
    """
    callback_event = request.get_json()
    po(callback_event)
    event_type = callback_event['eventType']

    if event_type == 'sms':
        messaging_api.send_message( from_ = callback_event['to'],
                                  to = callback_event['from'],
                                  text = 'Great job texting! Keep it up')
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    elif event_type == 'mms':
        messaging_api.send_message( from_ = callback_event['to'],
                                  to = callback_event['from'],
                                  text = 'Great job sending a mms. Here is a cute dog',
                                  media = ['https://s3.amazonaws.com/bwdemos/cute_dog.jpg'])
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    else:
        # Ignore everything else
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
