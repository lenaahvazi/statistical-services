import requests
import config
import json


def register():
    try:
        service_name = "statisticsCalculator"

        url = config.productCatalogURL + config.registrationEndpoint

        params = {
            "service_name": service_name
        }

        response = requests.get(url=url, params=params)
        status_code = response.status_code

        if status_code == 200:
            response_data = response.json()

            config.messageBrokerIP = response_data.get('messageBrokerIP')
            config.messageBrokerPort = response_data.get('messageBrokerPort')
            config.registerInterval = response_data.get('registerInterval')
            config.ip = response_data.get('ip')
            config.port = response_data.get('port')
            config.productCatalogURL = response_data.get('productCatalogURL')
            config.registrationEndpoint = response_data.get('registrationEndpoint')
            config.historicalDataIP = response_data.get('historicalDataIP')
            config.status = response_data.get('status')

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
