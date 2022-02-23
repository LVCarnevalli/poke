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
parser.add_argument("--add_user", help="")
parser.add_argument("--poke", help="")
parser.add_argument("--listen", help="", default=False, action=argparse.BooleanOptionalAction)
args = parser.parse_args()

first = False
storage = os.path.expanduser('~') + '/poke/data.json'
if not os.path.exists(os.path.dirname(storage)):
    first = True
    try:
        os.makedirs(os.path.dirname(storage))
    except OSError as exc: 
        if exc.errno != errno.EEXIST:
            raise

db = TinyDB(storage)
config = db.table('config')
users = db.table('users')

def get_config(key):
    return config.search(Query().key == key)[0]['value']

if first:
    response = requests.post('http://localhost:3000/user')
    if not response.ok:
        raise Exception('Error')
    hash = response.json()['hash']

    config.insert({'key': 'date_listen', 'value': ''})
    config.insert({'key': 'pause', 'value': 'false'})
    config.insert({'key': 'hash', 'value': hash})

    print('Share this hash with your friends: %s' %(hash,))

if args.add_user:
    add_user = args.add_user.split("=")
    users.insert({
        'alias': add_user[0], 'hash': add_user[1]
    })
    print('User added successfully.')

if args.poke:
    user_found = users.search(Query().alias == args.poke)
    response = requests.post('http://localhost:3000/poke', data=json.dumps({
        "from_hash": get_config('hash'),
        "to_hash":  user_found[0]['hash']
    }), headers={'content-type':'application/json'})
    if not response.ok:
        raise Exception('Error')
    print('User poke successfully.')

if args.listen:
    while (get_config('pause') == "false"):
        try:
            response = requests.get('http://localhost:3000/action?to_hash=%s&created_at=%s' %(get_config('hash'),get_config('date_listen'),))
            if not response.ok:
                raise Exception('Error')
            config.update({'key': 'date_listen', 'value': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')}, Query().key == 'date_listen')
            for action in response.json():
                from_hash = action['from_hash']
                user_found = users.search(Query().hash == from_hash)
                if len(user_found) > 0:
                    from_name = user_found[0]['alias']
                else:
                    from_name = from_hash
                if system == 'linux':
                    print("poke")
                else:    
                    os.system(f'osascript -e \'display notification "{from_name} poke you!"\'')

        except Exception as er:
            print(er)
        time.sleep(5)