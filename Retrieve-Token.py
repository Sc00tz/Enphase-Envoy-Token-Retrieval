# Originally from ha_steve on the Home Assistant forum
# https://community.home-assistant.io/t/enphase-local-api-with-firmware-7-x-my-setup/563828

import requests
import json
import sys

# --- CONFIGURATION ---
USER = 'email@example.com'
PASSWORD = 'password'
ENVOY_SERIAL = 'your_envoy_serial_number'

def get_enphase_token():
    """Fetches a local API token from Enphase Entrez."""
    
    # Use a session for better performance and cookie management
    with requests.Session() as session:
        try:
            # 1. Login to Enlighten
            login_data = {
                'user[email]': USER, 
                'user[password]': PASSWORD
            }
            login_url = 'https://enlighten.enphaseenergy.com/login/login.json'
            
            response = session.post(login_url, data=login_data)
            response.raise_for_status() # Raises an error for 4xx or 5xx responses
            
            auth_info = response.json()
            session_id = auth_info.get('session_id')
            
            if not session_id:
                print("Error: Could not find session_id in login response.")
                return

            # 2. Request the token from Entrez
            token_data = {
                'session_id': session_id, 
                'serial_num': ENVOY_SERIAL, 
                'username': USER
            }
            token_url = 'https://entrez.enphaseenergy.com/tokens'
            
            token_response = session.post(token_url, json=token_data)
            token_response.raise_for_status()
            
            # The response text itself is the JWT token
            return token_response.text.strip()

        except requests.exceptions.RequestException as e:
            print(f"Network or Auth Error: {e}")
            return None

if __name__ == "__main__":
    token = get_enphase_token()
    if token:
        print("Successfully retrieved token:")
        print(token)
    else:
        sys.exit(1)
