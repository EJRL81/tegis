from flask import Flask, request, jsonify, render_template
import json
import requests
import subprocess
app = Flask(__name__)

requests.packages.urllib3.disable_warnings()

api_url = "https://192.168.43.182/restconf/"
headers = {"Accept": "application/yang-data+json", "Content-type": "application/yang-data+json"}
basicauth = ("cisco", "cisco123!")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_interfaces', methods=['GET'])
def get_interfaces():
    module = "data/ietf-interfaces:interfaces"
    resp = requests.get(f'{api_url}{module}', auth=basicauth, headers=headers, verify=False)
    if resp.status_code == 200:
        return jsonify(resp.json())
    else:
        return jsonify({"error": f"Error al realizar la consulta del modulo {module}"}), resp.status_code

@app.route('/get_restconf_native', methods=['GET'])
def get_restconf_native():
    module = "data/Cisco-IOS-XE-native:native"
    resp = requests.get(f'{api_url}{module}', auth=basicauth, headers=headers, verify=False)
    if resp.status_code == 200:
        return jsonify(resp.json())
    else:
        return jsonify({"error": f"Error al consumir la API para el modulo {module}"}), resp.status_code

@app.route('/get_banner', methods=['GET'])
def get_banner():
    module = "data/Cisco-IOS-XE-native:native/banner/motd"
    resp = requests.get(f'{api_url}{module}', auth=basicauth, headers=headers, verify=False)
    if resp.status_code == 200:
        return jsonify(resp.json())
    else:
        return jsonify({"error": f"Error al consumir la API para el modulo {module}"}), resp.status_code

@app.route('/put_banner', methods=['POST'])
def put_banner():
    banner = {
        "Cisco-IOS-XE-native:motd": {
            "banner": request.form['banner']
        }
    }
    module = "data/Cisco-IOS-XE-native:native/banner/motd"
    resp = requests.put(f'{api_url}{module}', data=json.dumps(banner), auth=basicauth, headers=headers, verify=False)
    if resp.status_code == 204:
        return jsonify({"message": "Actualización exitosa"})
    else:
        return jsonify({"error": "Error, no se puede realizar la actualización al modulo"}), resp.status_code

@app.route('/post_loopback', methods=['POST'])
def post_loopback():
    dloopback = {
        "ietf-interfaces:interface": {
            "name": request.form['loopback_name'],
            "description": request.form['description'],
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": request.form['ip'],
                        "netmask": request.form['netmask']
                    }
                ]
            }
        }
    }
    module = "data/ietf-interfaces:interfaces"
    resp = requests.post(f'{api_url}{module}', auth=basicauth, headers=headers, data=json.dumps(dloopback), verify=False)
    if resp.status_code == 201:
        return jsonify({"message": f'Se insertó correctamente {dloopback}'})
    else:
        return jsonify({"error": f"Error al insertar elemento al módulo {module}"}), resp.status_code

@app.route('/del_loopback', methods=['POST'])
def del_loopback():
    module = f"data/ietf-interfaces:interfaces/interface={request.form['loopback_name_del']}"
    resp = requests.delete(f'{api_url}{module}', auth=basicauth, headers=headers, verify=False)
    if resp.status_code == 204:
        return jsonify({"message": "Se eliminó correctamente"})
    else:
        return jsonify({"error": "Error al eliminar"}), resp.status_code

@app.route('/get_router_config', methods=['GET'])
def get_router_config():
    module = "data/Cisco-IOS-XE-native:native/router"
    resp = requests.get(f'{api_url}{module}', auth=basicauth, headers=headers, verify=False)
    if resp.status_code == 200:
        return jsonify(resp.json())
    else:
        return jsonify({"error": f"Error al obtener la configuración del router {module}"}), resp.status_code


@app.route('/add_network', methods=['POST'])
def add_network():
    try:
        network_ip = request.form['network_ip']
        module = "data/Cisco-IOS-XE-native:native"

        # Construir el JSON para agregar la red
        network_config = {
            "Cisco-IOS-XE-native:native": {
                "router": {
                    "rip": {
                        "Cisco-IOS-XE-rip:rip": {
                            "network": {
                                "ip": network_ip
                            }
                        }
                    }
                }
            }
        }

        # Enviar solicitud PUT a la API RESTCONF
        resp = requests.put(f'{api_url}{module}', data=json.dumps(network_config), auth=basicauth, headers=headers, verify=False)

        if resp.status_code == 204:
            return jsonify({"message": f"Se agregó la red {network_ip} correctamente"})
        else:
            return jsonify({"error": f"Error al agregar la red {network_ip}: {resp.text}"}), resp.status_code

    except KeyError:
        return jsonify({"error": "Datos incompletos. Falta el campo 'network_ip' en el formulario"}), 400

    except Exception as e:
        return jsonify({"error": f"Error al procesar la solicitud: {str(e)}"}), 500


@app.route('/remove_network', methods=['POST'])
def remove_network():
    try:
        network_ip = request.form['network_ip']
        module = f"data/Cisco-IOS-XE-native:native/router/rip/network/{network_ip}"

        # Enviar solicitud DELETE a la API RESTCONF
        resp = requests.delete(f'{api_url}{module}', auth=basicauth, headers=headers, verify=False)

        if resp.status_code == 204:
            return jsonify({"message": f"Se eliminó la red {network_ip} correctamente"})
        else:
            return jsonify({"error": f"Error al eliminar la red {network_ip}: {resp.text}"}), resp.status_code

    except KeyError:
        return jsonify({"error": "Datos incompletos. Falta el campo 'network_ip' en el formulario"}), 400

    except Exception as e:
        return jsonify({"error": f"Error al procesar la solicitud: {str(e)}"}), 500


@app.route('/test_connectivity', methods=['POST'])
def test_connectivity():
    try:
        target_ip = request.form['target_ip']
        response = subprocess.run(['ping', '-c', '4', target_ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  text=True)

        if response.returncode == 0:
            return jsonify({"message": f"Conectividad exitosa con {target_ip}", "output": response.stdout})
        else:
            return jsonify({"error": f"Error en la conectividad con {target_ip}", "output": response.stderr}), 400
    except Exception as e:
        return jsonify({"error": f"Error al realizar la prueba de conectividad: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
