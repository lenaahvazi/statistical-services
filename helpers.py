import requests
import config
import json


def update_config_file(updates):
    lines = []
    with open(config.CONFIG_FILE_PATH, 'r') as file:
        lines = file.readlines()

    with open(config.CONFIG_FILE_PATH, 'w') as file:
        for line in lines:
            for key, value in updates.items():
                if line.startswith(f"{key} ="):
                    if isinstance(value, str):
                        file.write(f"{key} = '{value}'\n")
                    else:
                        file.write(f"{key} = {value}\n")
                    break
            else:
                file.write(line)


def register():
    try:
        url = config.productCatalogURL + config.registrationEndpoint

        params = {
            "service_name": config.serviceName
        }

        response = requests.get(url=url, params=params)
        status_code = response.status_code

        if status_code == 200:
            response_data = response.json()

            updates = {
                'messageBrokerIP': response_data.get('messageBrokerIP', config.messageBrokerIP),
                'messageBrokerPort': response_data.get('messageBrokerPort', config.messageBrokerPort),
                'registerInterval': response_data.get('registerInterval', config.registerInterval),
                'ip': response_data.get('ip', config.ip),
                'port': response_data.get('port', config.port),
                'productCatalogURL': response_data.get('productCatalogURL', config.productCatalogURL),
                'registrationEndpoint': response_data.get('registrationEndpoint', config.registrationEndpoint),
                'historicalDataIP': response_data.get('historicalDataIP', config.historicalDataIP),
                'status': response_data.get('status', config.status)
            }

            update_config_file(updates)

            print("Configuration saved.")
            return "Configuration saved.", 200

        else:
            print(f"Failed to retrieve data: Status code {status_code}")
            return f"Failed to retrieve data: Status code {status_code}", status_code

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return f"Request error: {e}", 500

    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return f"JSON decode error: {e}", 500

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return f"An unexpected error occurred: {e}", 500
