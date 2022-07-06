# https://docs.oracle.com/en-us/iaas/tools/python-sdk-examples/2.74.0/core/update_instance.py.html

import oci, logging

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', filename="update.log", filemode='w', level=logging.DEBUG, )
logging.getLogger().addHandler(logging.StreamHandler())
logger = logging.getLogger(__name__)
log_level = logging.INFO
log_level = logging.DEBUG
logger.setLevel(log_level)

def init_config():
    config = oci.config.from_file("~/.oci/config", "j5a")
    return config

config = init_config()
core_client = oci.core.ComputeClient(config)
i_id = "ocid1.instance.oc1.sa-santiago-1.anzwgljrnzdi63icqlryjtrrdpnrb7tjwm73b5zprnpjgzku7dwelvdlga6q"
instance = core_client.get_instance(instance_id = i_id)
assert instance, f'No instance found'
i_data = instance.data
logger.debug(f'Instance shape is: {i_data.shape}')
logger.debug(f'Instance shape details is: {i_data.shape_config}')
logger.debug(f'Instance launch options is: {i_data.launch_options}')
try:
    update_instance_response = core_client.update_instance(instance_id=i_id,
        update_instance_details=oci.core.models.UpdateInstanceDetails(
                shape="VM.Standard3.Flex",
                launch_options=oci.core.models.UpdateLaunchOptions(
                    network_type= oci.core.models.UpdateLaunchOptions.NETWORK_TYPE_PARAVIRTUALIZED,
                    #boot_volume_type = i_data.launch_options.boot_volume_type,
                    #is_pv_encryption_in_transit_enabled = i_data.launch_options.is_pv_encryption_in_transit_enabled
                    )))
except oci.exceptions.ServiceError as err:
    logger.error(f'Unexpected error {err}')
assert update_instance_response.data, f'No response data'
assert update_instance_response.data.status == 200, f'Unexpected status: {update_instance_response.data.status}'
logger.debug(f'Update instance {update_instance_response.data}')
