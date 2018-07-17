import requests



def get_venmos():
    vens = requests.get("https://venmo.com/api/v5/public?limit=1000")
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


def check_ven(json):
    if any(x in json['message'].lower() for x in ('weed', 'meth', 'heroin', 'booze', 'sex', 'alcohol', 'pills', 'drank', 'marijuana', 'coke', 'cocaine')):
        return json['message']
    else: 
        return False


for ven in vens:
    if check_ven(ven):
        print(summarize(ven))
