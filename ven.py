import requests



def get_venmos():
    vens = requests.get("https://venmo.com/api/v5/public?limit=10")
    return vens.json()['data']

vens = get_venmos()

print(vens[0]['actor']['name'])