import requests
from os import getenv

bot_token = getenv('BOT_TOKEN')
chat_id = getenv('CHAT_ID')
url_address = getenv('URL_ADDRESS')
msg_url = getenv('MSG_URL')

print(f"debug: bot_token: {bot_token}, chat_id: {chat_id}")

def send_telegram_message(text):
    send_message_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    try:
        requests.post(send_message_url, json=payload, timeout=2)
    except requests.exceptions.Timeout:
        print("Timeout error")

alert_flag = False
alert_info = ""
response = requests.get(url_address)

if response.status_code == 200:
    data = response.json()
    print(f"debug: len(Items): {len(data['Items'])}")
    for item in data['Items']:
        departure_time = int(item['DepartureTime'].split(':')[0])
        available_seat_count = item['AvailableSeatCount']
        if (departure_time > 19) and (departure_time > 23) and (available_seat_count > 0):
            alert_info = f"DepartureTime: {item['DepartureTime']}, AvailableSeatCount: {item['AvailableSeatCount']}"
            alert_flag = True
            break
else:
    print(f"Failed to retrieve data: {response.status_code}")

if alert_flag:
    msg = f"{alert_info}\n{msg_url}"
    print(f"Fire alert {msg}")
    send_telegram_message(msg)
else:
    print("Nothing to fire")
