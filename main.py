import json
import  requests
dic_data = {'router':[
    {"modelo": 'CAT2323',
     "modelo":'CAT4223'}],
    'switch':[
        {"name":'CR2323',
         "vendor":'cisco'}
    ]
}



def gets_ip():

    with open("./data/api2.json",'w') as files:
        response = requests.get('http://ip-api.com/json/24.85.0.1')
        responses = response.json()
        json.dump(responses, files, indent=4, sort_keys=True)


def formar_json():
    print(json.dumps(dic_data, indent=2))
with open("./data/infraestructure1.json",'w') as file:
    json.dump(dic_data, file, indent=4, sort_keys=True)

if __name__ == '__main__':
    gets_ip()