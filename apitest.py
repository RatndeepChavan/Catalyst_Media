import requests, json, sys

# Run this file ini terminal to check api working

ar = sys.argv[1] if len(sys.argv)>1 else False

# Provide valid email and password here
auth = ('rr@rr.rr', 'rr')

if ar :
    if  ar == '1' :
        u = "http://127.0.0.1:8000/api/enb/"
        data = {'st' : True}

    elif  ar == '2' :
        u = "http://127.0.0.1:8000/api/dis/"
        data = {'st' : False}

    elif  ar == '3' :
        u = "http://127.0.0.1:8000/api/bal/"
        data = ''

    elif  ar == '4' :
        u = "http://127.0.0.1:8000/api/add/"
        data = 100

    elif  ar == '5' :
        u = "http://127.0.0.1:8000/api/rmv/"
        data = 100

    js = json.dumps(data)
    r = requests.put(url=u, data=js, auth=auth)

    print(r.json())

else :
    print('1 - enable wallet')
    print('2 - disable wallet')
    print('3 - Balance')
    print('4 - add money')
    print('5 - remove money')

