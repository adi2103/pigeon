from http.client import HTTPException
import os
import logging
from flask import Flask, jsonify, request
from flask.helpers import send_from_directory
from flask_cors import CORS, cross_origin
from twilio.rest import Client

TESTING_CALL_SID = "TESTING_CALL_SID"

log = logging.getLogger("pigeon")
log.setLevel(logging.DEBUG)
logging.basicConfig()

def create_app():
    app = Flask(
        __name__,
        static_folder='../react-app/build',
        static_url_path=''
    )
    CORS(app)

    @app.route('/')
    @cross_origin()
    def serve():
        """ Handle the home page """
        return send_from_directory(app.static_folder, 'index.html')

    @app.route('/calls', methods = ['POST'])
    @cross_origin()
    def handle_calls():
        """ Handle call creation requests """
        log.info("Received POST /calls request")
        phone_number = request.json.get('phone_number')
        message = request.json.get('message')

        log.info(f'Starting a voice call to {phone_number}')
        log.info(f'Sending the a voice message {message}')

        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        host = os.environ['HOST']
        client = Client(account_sid, auth_token)

        try:
            call = client.calls.create(
                twiml=f'<Response><Say>{message}</Say></Response>',
                to=phone_number,
                from_='+17432004167',
                status_callback=f'{host}/status',
                status_callback_event=['ringing', 'answered', 'completed'],
                status_callback_method='POST',
            )
        except Exception:
            log.exception('Error while creating twilio call', exc_info=True)
            raise HTTPException('Error while creating twilio call')
        response = jsonify({'call_sid': call.sid})
        if call.sid and app.config["TESTING"] == True:
            response = jsonify({'call_sid': TESTING_CALL_SID})
        return response

    @app.route('/status', methods = ['POST'])
    @cross_origin()
    def handle_status():
        """ Handle call status update requests """
        log.info("Received POST /status request")
        call_sid = request.form.get('CallSid')
        call_status = request.form.get('CallStatus')
        log.info(f'Call {call_sid} is {call_status}')
        return "Status recorded"

    return app
