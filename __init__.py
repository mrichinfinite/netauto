__copyright__ = "Copyright (c) 2018 Cisco Systems. All rights reserved."

import json
import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def task(env):
    """
    Replace this docstring with your documentation. 
    
    This task is run by the bdblib library, full doc and examples at: 
    https://scripts.cisco.com/doc/
    Browse more examples in BDB starting with "bdblib_":
    https://scripts.cisco.com/ui/browse/used/0/bdblib_

    """
    file_name = os.path.dirname(os.path.realpath(__file__))+"/static_steps.json"
    logger.info("Steps Json File {}".format(file_name))
    steps_json= {}
    with open(file_name,'r') as file_content:
        steps_json = json.load(file_content)
    
    logger.debug("Json retreived from the file {}".format(steps_json))
    return steps_json
    