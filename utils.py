import requests, json # type: ignore

banner = '''
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⠶⠛⠛⠛⠶⣤⡀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⠟⠋⢁⣠⣴⣶⣶⣶⣬⣿⣆⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⡾⠟⠉⢀⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀
⠀⠀⠀⠀⠀⠀⠀⢀⣠⡴⠟⠋⠁⠀⠀⠺⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀
⠀⠀⠀⠀⢀⣴⠾⠛⠉⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⠀       pumpWatch - A pump.fun token monitor
⠀⠀⢀⡾⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢈⣿⣿⣿⣿⣿⣿⣿⠿⠋⠀⠀⠀         created by Umair Nehri(@0x9747)
⠀⢀⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣾⠿⢿⣿⣿⡿⠟⠋⠀⠀⠀⠀⠀⠀
⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⡾⠛⢉⣠⣴⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢿⡄⠐⢦⣤⣤⣴⣾⠿⠛⣁⣤⡾⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠻⢦⣄⣀⠉⣉⣀⣴⠾⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠉⠛⠛⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
'''

def load_notifiers(file_path="notifier.json"):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Failed to load notifiers from file: {e}")
        return {}

def send_notification(webhook_url, message):
    try:
        if "discord" in webhook_url:
            response = requests.post(webhook_url, json={"username": "pumpWatch", "content": message})
        else:
            response = requests.post(webhook_url, json={"text": message})
        if response.status_code != 200 and response.status_code != 203 and response.status_code != 204:
            print(f"Failed to send notification. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending notification: {e}")

def notify_new_token(message, notifiers):
    if "discord" in notifiers and notifiers["discord"]:
        send_notification(notifiers["discord"], message)
    if "slack" in notifiers and notifiers["slack"]:
        send_notification(notifiers["slack"], message)