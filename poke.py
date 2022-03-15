import requests
import time
from datetime import datetime, timezone 
import os
from tinydb import TinyDB, Query
import argparse
import json
import platform
system = platform.system().lower()

parser = argparse.ArgumentParser("poke")
parser.add_argument("--add_user", help="Add user with token and alias.")
parser.add_argument("--get_users", help="Get all users.", default=False, action='store_true')
parser.add_argument("--poke_url", help="Url poke server.")
parser.add_argument("--user", help="Alias of user.")
parser.add_argument("--listen", help="", default=False, action='store_true')
args = parser.parse_args()

storage = os.path.expanduser('~') + '/poke/data.json'
db = TinyDB(storage)
config = db.table('config')
users = db.table('users')

def get_config(key):
    return config.search(Query().key == key)[0]['value']

if args.poke_url:
    poke_url = args.poke_url
else:
    poke_url = get_config('poke_url')

if not config.search(Query().key == "first_app"):
    response = requests.post('%s/user' %(poke_url,))
    if not response.ok:
        raise Exception('Error')
    hash = response.json()['hash']

    config.insert({'key': 'date_listen', 'value': ''})
    config.insert({'key': 'hash', 'value': hash})
    config.insert({'key': 'poke_url', 'value': poke_url})
    config.insert({'key': 'first_app', 'value': 'false'})

    print('Share this hash with your friends: %s' %(hash,))

if args.get_users:
    print(users.all())

if args.add_user:
    add_user = args.add_user.split("=")
    users.insert({
        'alias': add_user[0], 'hash': add_user[1]
    })
    print('User added successfully.')

if args.user:
    user_found = users.search(Query().alias == args.user)
    response = requests.post('%s/poke' %(poke_url,), data=json.dumps({
        "from_hash": get_config('hash'),
        "to_hash":  user_found[0]['hash']
    }), headers={'content-type':'application/json'})
    if not response.ok:
        raise Exception('Error')
    print('User poke successfully.')

if args.listen:
    while (true):
        try:
            response = requests.get('%s/action?to_hash=%s&created_at=%s' %(poke_url,get_config('hash'),get_config('date_listen'),))
            if not response.ok:
                raise Exception('Error')
            config.update({'key': 'date_listen', 'value': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')}, Query().key == 'date_listen')
            for action in response.json():
                from_hash = action['from_hash']
                user_found = users.search(Query().hash == from_hash)
                if user_found:
                    from_name = user_found[0]['alias']
                    if system == 'linux':
                        os.system(f'notify-send "{from_name} poke you!"')
                    else:
                        os.system(f'osascript -e \'display notification "{from_name} poke you!" with title "Poke" sound name "default"\'')

        except Exception as er:
            print(er)
        time.sleep(5)
