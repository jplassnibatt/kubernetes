#!/usr/bin/env python -u
import logging
import sys
import os
import common

from kubernetes import client
from kubernetes.client.rest import ApiException


logging.basicConfig(stream=sys.stderr, level=logging.INFO,
                    format='%(levelname)s: %(name)s: %(message)s')
log = logging.getLogger('kubernetes-model-source')


def main():

    pod_name = os.environ.get('RD_CONFIG_NAME')
    namespace = os.environ.get('RD_CONFIG_NAMESPACE')

    if not pod_name:
        [pod_name, namespace, container] = common.get_core_node_parameter_list()

    common.connect()

    try:
        api = client.CoreV1Api()

        api_response = api.read_namespaced_pod(
            name=pod_name,
            namespace=namespace)

        print(common.parseJson(api_response.status))

#         replicas = api_response.status.replicas
#         r_replicas = api_response.status.ready_replicas
#         u_replicas = api_response.status.unavailable_replicas
#
#         if(u_replicas is not None):
#             log.error(
#                 "unavailable replicas on the deployment: %s\n", u_replicas
#             )
#             sys.exit(1)
#
#         if (replicas != r_replicas):
#             log.error(
#                 "ready replicas doesn't match with replicas: %s\n", r_replicas
#             )
#             sys.exit(1)

    except ApiException:
        log.exception("Exception deleting deployment:")
        sys.exit(1)


if __name__ == '__main__':
    main()
