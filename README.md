# pigeon
A light weight voice messaging app

### Key points

- Deployment host: Heroku
- Deployed URL: https://pigeon-ufonia.herokuapp.com
- Set up live config variables using the below command:
  ```bash
  heroku config:set HOST=https://pigeon-ufonia.herokuapp.com TWILIO_ACCOUNT_SID=ACebd6cd2cf151d10cc31d86e6ea3a8219 TWILIO_AUTH_TOKEN=xxxxxxxxxx --app pigeon-ufonia```
- `TWILIO_AUTH_TOKEN` keeps changing
- For any new recipient phone number, please get the number first verified in the the Twilio account