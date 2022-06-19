from http.client import HTTPException
import os
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from twilio.rest import Client

TESTING_CALL_SID = "TESTING_CALL_SID"

log = logging.getLogger("pigeon")
log.setLevel(logging.DEBUG)
logging.basicConfig()

def create_app():
    app = Flask(
        __name__,
        static_folder='../react-app/build',
        static_url_path='/'
    )
    CORS(app)

    @app.route('/calls', methods = ['POST'])
    def handle_calls():
        """ Handle call creation requests """
        log.info("Received POST /calls request")
        phone_number = request.json.get('phone_number')
        message = request.json.get('message')

        log.info(f'Starting a voice call to {phone_number}')
        log.info(f'Sending the a voice message {message}')

        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        client = Client(account_sid, auth_token)

        try:
            call = client.calls.create(
                twiml=f'<Response><Say>{message}</Say></Response>',
                to=phone_number,
                from_='+17432004167',
                status_callback='https://2bfa-2a00-23c6-f08b-8001-f120-8aeb-1fe-2b1d.eu.ngrok.io/status',
                status_callback_event=['ringing', 'answered', 'completed'],
                status_callback_method='POST',
            )
        except Exception:
            log.exception('Error while creating twilio call', exc_info=True)
            raise HTTPException('Error while creating twilio call')
        response = jsonify({'call_sid': call.sid})
        if call.sid and app.config["TESTING"] == True:
            response = jsonify({'call_sid': TESTING_CALL_SID})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    @app.route('/status', methods = ['POST'])
    def handle_status():
        """ Handle call status update requests """
        log.info("Received POST /status request")
        call_sid = request.form.get('CallSid')
        call_status = request.form.get('CallStatus')
        log.info(f'Call {call_sid} is {call_status}')
        return "Status recorded"

    return app
