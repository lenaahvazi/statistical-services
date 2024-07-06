import json
import requests
import config


def register():
    try:
        service_name = "statisticsCalculator"

        url = config.productCatalogURL + config.registrationEndpoint

        params = {
            "service_name": service_name
        }

        response = requests.get(url, params=params)
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

            return json.dumps({"message": "DB connector configuration written to config.json"}), 200

        else:
            return json.dumps({"error": f"Failed to retrieve data: Status code {status_code}"}), status_code

    except requests.exceptions.RequestException as e:
        return json.dumps({"error": f"Request error: {e}"}), 500

    except json.JSONDecodeError as e:
        return json.dumps({"error": f"JSON decode error: {e}"}), 500

    except Exception as e:
        return json.dumps({"error": f"An unexpected error occurred: {e}"}), 500
