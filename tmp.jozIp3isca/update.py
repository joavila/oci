# https://docs.oracle.com/en-us/iaas/tools/python-sdk-examples/2.74.0/core/update_instance.py.html

import oci, logging, os

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', filename="update.log", filemode='w', level=logging.DEBUG, )
logging.getLogger().addHandler(logging.StreamHandler())
logger = logging.getLogger(__name__)
log_level = logging.INFO
log_level = logging.DEBUG
logger.setLevel(log_level)

def init_config():
    # ENV
    CONFIG_FILE = os.getenv('CONFIG_FILE', '~/.oci/config')
    PROFILE = os.getenv('PROFILE', 'j5a')
    config = oci.config.from_file(CONFIG_FILE, PROFILE)
    return config

def main():
    # Handy
    TARGETTED_NETWORK_TYPE = oci.core.models.UpdateLaunchOptions.NETWORK_TYPE_PARAVIRTUALIZED
    TARGETTED_SHAPE = "VM.Standard3.Flex"
    # Main
    config = init_config()
    core_client = oci.core.ComputeClient(config)
    for affected_instance_id in [ "ocid1.instance.oc1.sa-santiago-1.anzwgljrnzdi63icqlryjtrrdpnrb7tjwm73b5zprnpjgzku7dwelvdlga6q" ]:
        instance = core_client.get_instance(instance_id = affected_instance_id)
        assert instance, f'No instance found'
        assert instance.data, f'No instance data found'
        instance_data = instance.data
        logger.debug(f'Current instance id is: {instance_data.id}')
        logger.debug(f'Current instance shape details are: {instance_data.shape_config}')
        try:
            if TARGETTED_NETWORK_TYPE == instance_data.launch_options.network_type and TARGETTED_SHAPE == instance_data.shape:
                logger.warning(f'Shape and network type already set to expected value')
                continue
            elif TARGETTED_NETWORK_TYPE == instance_data.launch_options.network_type:
                logger.debug(f'Network type already set to expected value: {instance_data.launch_options}')
                new_instance_details=oci.core.models.UpdateInstanceDetails(shape=TARGETTED_SHAPE)
            elif TARGETTED_SHAPE == instance_data.shape_config.shape:
                logger.debug(f'Shape already set to expected value: {instance_data.shape}')
                new_launch_options = oci.core.models.UpdateLaunchOptions(network_type=TARGETTED_NETWORK_TYPE)
                new_instance_details = oci.core.models.UpdateInstanceDetails(launch_options=new_launch_options)
            else:
                logger.debug(f'Current shape is: {instance_data.shape_config.shape}')
                logger.debug(f'Current network type is: {instance_data.launch_options}')
                new_launch_options = oci.core.models.UpdateLaunchOptions(network_type=TARGETTED_NETWORK_TYPE)
                new_instance_details = oci.core.models.UpdateInstanceDetails(shape=TARGETTED_SHAPE, launch_options=new_launch_options)

            update_instance_response = core_client.update_instance(instance_id=affected_instance_id, update_instance_details=new_instance_details)
            assert update_instance_response.data, f'No response data'
            assert update_instance_response.data.status == 200, f'Unexpected status is: {update_instance_response.data.status}'
            logger.debug(f'Updated instance response is: {update_instance_response.data}')
        except oci.exceptions.ServiceError as err:
            logger.error(f'Unexpected error {err}')

if __name__ == "__main__":
        main()