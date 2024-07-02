import json
import requests
import subprocess
requests.packages.urllib3.disable_warnings()


def get_interfaces():
    module = "data/ietf-interfaces:interfaces"
    resp = requests.get(f'{api_url}{module}', auth=basicauth, headers=headers, verify=False)
    print(json.dumps(resp.json(), indent=4))
    data_json = resp.json()

    for key, valor in data_json.items():
        print(f'Nombre de la interface: {valor["interface"][0]["name"]}')
        print(f'Descripción de la interface: {valor["interface"][0]["description"]}')
        print(f'Status de la interface: {valor["interface"][0]["enabled"]}')


    else:
        print(f'Error al realizar la consulta del modulo {module}')

def get_restconf_native():
    module = "data/Cisco-IOS-XE-native:native"
    resp = requests.get(f'{api_url}{module}', auth=basicauth, headers=headers, verify=False)
    print(json.dumps(resp.json(), indent=4))

def get_banner():
    module = "data/Cisco-IOS-XE-native:native/banner"
    resp = requests.get(f'{api_url}{module}', auth=basicauth, headers=headers, verify=False)
    print(json.dumps(resp.json(), indent=4))

def test_connectivity():
    try:
        target_ip = requests.form['target_ip']
        response = subprocess.run(['ping', '-c', '4', target_ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  text=True)

        if response.returncode == 0:
            return jsonify({"message": f"Conectividad exitosa con {target_ip}", "output": response.stdout})
        else:
            return jsonify({"error": f"Error en la conectividad con {target_ip}", "output": response.stderr}), 400
    except Exception as e:
        return jsonify({"error": f"Error al realizar la prueba de conectividad: {str(e)}"}), 500
if __name__ == '__main__':
    # module:operations, data
    api_url = "https://192.168.0.10/restconf/"
    headers = {"Accept": "application/yang-data+json",
               "Content-type": "application/yang-data+json"
               }
    basicauth = ("cisco", "cisco123!")

get_interfaces()
get_restconf_native()
get_banner()