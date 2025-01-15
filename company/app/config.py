from dapr.clients import DaprClient
import logging

from fastapi import HTTPException

logger = logging.getLogger(__name__)
DAPR_CONFIGURATION_STORE = 'configstore'

def get_configuration(config):
    """
    Fetch configuration values from Dapr configuration API.

    Returns:
        dict: A dictionary containing the configuration values.
    """
    
    config_data = []
    
    try:
        with DaprClient() as client:
            print("dapr client created")
            response = client.get_configuration(store_name="configstore", keys=config)

            config = {key: response.items[key].value for key in config}
            return config
            
    except Exception as e:
        logger.error("Error fetching configuration from Dapr: %s", e, exc_info=True)
        raise HTTPException(status_code=500)
