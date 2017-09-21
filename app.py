import os
import sys
import pprint
import json

from bw_clients import *
from flask import Flask, request, render_template
from quick_deploy import *

app = Flask(__name__)

def po(o):
    """
    Prints things to console much more nicely than the default print
    """
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(o)

# Global variable for app name
bw_application_id = ''

# Just a nice hello world :)
@app.route('/')
def hello():
    global bw_application_id
    bw_application_id = check_or_create_application(request, bw_application_id)
    my_numbers = check_or_create_phone_number(bw_application_id, '910')
    numbers = ''
    for number in my_numbers:
        numbers = numbers + number['national_number'] + '\n'
    return render_template('index.html', numbers_list=my_numbers)

@app.route(call_path, methods=['POST'])
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

@app.route(message_path, methods=['POST'])
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
