from hypchat import HypChat
from utils import get_config


def get_client(config):
    client = HypChat(config.get('hipchat', 'token'))
    return client


def message_room(client, room_name, message):
    try:
        room = client.get_room(room_name)
        room.message(message)
    except Exception as e:
        print e


def main():
    config = get_config('DEV')
    client = get_client(config)
    message_room(client, 'My Favorite Room', "I'M A ROBOT!")
