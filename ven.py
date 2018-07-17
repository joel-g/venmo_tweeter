import requests



def get_venmos():
    vens = requests.get("https://venmo.com/api/v5/public?limit=10")
    return vens.json()['data']

def summarize(json):
    actor = json['actor']['name']
    target = json['transactions'][0]['target']['name']
    method = json['type']
    message = json['message']
    if method == 'payment':
        method = 'paid'
    elif method == 'charge':
        method = 'charged'
    return actor + " " + method + " " + target + " for " + message

vens = get_venmos()

actor = vens[0]['actor']['name']

print(actor)

target = vens[0]['transactions'][0]['target']['name']

print(target)

message = vens[0]['message']

print(message)

print(summarize(vens[0]))
