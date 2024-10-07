# Originally from ha_steve on the Home Assistant forum
# https://community.home-assistant.io/t/enphase-local-api-with-firmware-7-x-my-setup/563828

import json
import requests

# REPLACE ITEMS BELOW 
user='email@example.com'
password='password'
envoy_serial='your_envoy_serial_number'
# DO NOT CHANGE ANYTHING BELOW

data = {'user[email]': user, 'user[password]': password}
response = requests.post('https://enlighten.enphaseenergy.com/login/login.json?',data=data)
response_data = json.loads(response.text)
data = {'session_id': response_data['session_id'], 'serial_num': envoy_serial, 'username':user}
response = requests.post('https://entrez.enphaseenergy.com/tokens', json=data)
token_raw = response.text
print(token_raw)
