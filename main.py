import requests
import os
# from dotenv import load_dotenv

# load_dotenv()

bot_token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')

print(f"debug: bot_token: {bot_token}, chat_id: {chat_id}")

def send_telegram_message():
    send_message_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    # TODO: change text
    payload = {
        "chat_id": chat_id,
        "text": f"https://safar724.com/bus/tehran-tabriz?date=1402-12-02, {alert_info}"
    }
    try:
        requests.post(send_message_url, json=payload, timeout=2)
    except requests.exceptions.Timeout:
        print("Timeout error")

# TODO: change url
url = 'https://safar724.com/bus/getservices?origin=11320000&destination=26310000&date=1402-12-02'
response = requests.get(url)
alert = False
alert_info = ""

if response.status_code == 200:
    data = response.json()
    for item in data['Items']:
        departure_time = int(item['DepartureTime'].split(':')[0])
        available_seat_count = item['AvailableSeatCount']

        if (departure_time > 19) and (available_seat_count > 0):
            alert_info = f"DepartureTime: {item['DepartureTime']}, AvailableSeatCount: {item['AvailableSeatCount']}"
            print(alert_info)
            alert = True
            break
else:
    print(f"Failed to retrieve data: {response.status_code}")

if alert:
    print("Fire alert")
    send_telegram_message()
else:
    print("Nothing to fire")
