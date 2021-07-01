# Copyright 2021 IBA IT Park FE
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#
# Refer to the README and COPYING files for full details of the license
#
from __future__ import absolute_import

import json
import logging
from handlers.responses_utils import get_entity

PORT_ID = 'port_id'

def custom_ports(ports_func):
    def inner(nb_db, content, parameters):
      received_port = get_entity(content, 'port')
      logging.info("Content: {}".format(content))
      logging.info("Parameters: {}".format(parameters))
      logging.info("Received_port: {}".format(received_port))
      custom_db = __custom_ports()
      received_port.update( custom_db.get(parameters.get(PORT_ID),
                custom_db.get(received_port.get('mac_address'), {})) )
      logging.info("New Received_port: {}".format(received_port))
      new_content = json.dumps({'port': received_port})
      logging.info("NewContent: {}".format(new_content))
      port = ports_func(nb_db, new_content, parameters)
      logging.info("Port: {}".format(port))
      return port
    return inner

def __custom_ports():
    data = {}
    try:
        with open('/etc/ovirt-provider-ovn/custom_ports.json') as ports_file:
                data = json.load(ports_file)
    except IOError:
      pass
    return data

