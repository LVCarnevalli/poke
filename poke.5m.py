#!/usr/local/bin/python3
# <bitbar.title>poke</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author.github>LVCarnevalli</bitbar.author.github>
# <bitbar.author>LVC</bitbar.author>
# <bitbar.desc>Poke</bitbar.desc>
import os
import ast

def bash(command):
    output = os.popen(command).read()
    return output

print("poke | color='black'")
print("---")

out = bash('/usr/local/bin/python3 ~/poke/poke.py --get_users')
for u in ast.literal_eval(out):
    print(f"{u['alias']} | bash=/usr/local/bin/python3 param1={os.getenv('HOME')}/poke/poke.py param2=--user param3={u['alias']} terminal=false")