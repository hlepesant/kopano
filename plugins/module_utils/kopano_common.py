from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible.module_utils.six.moves import configparser

import traceback
import sys

kopano_found = False
E_IMP_ERR = None
NotFoundError = None
helpers = None

try:
  import kopano
  kopano_found = True
except ImportError:
  E_IMP_ERR = traceback.format_exc()
  kopano_found = False


def kopano_common_argument_spec():
  """
  Returns a dict containing common options shared across the kopano modules
  """
  options = dict(
    server_socket=dict(type='str', default=None),
    sslkey_file=dict(type='str', default=None),
    sslkey_pass=dict(type='str', default=None, no_log=True),
    # config=dict(type='str', default=None),
    # auth_user=dict(type='str', default=None),
    # auth_pass=dict(type='str', default=None, no_log=True),
    # options=dict(type='str', default=None),
    # parse_args=dict(type='str', default=False),
  )
  return options

class KopanoHelpers():
  """
  Class containing helper functions for Kopano modules
  """

  def __init__(self, module):
    self.module = module

  def use_default_location(self, module):
    if module.params['server_socket'] is not None:
      return False
    return True

  def connect(self):
    default_location = self.use_default_location(self.module)

    if default_location:
      k = kopano.Server()
    else:
      k = kopano.server(
        module.params['server_socket'],
        module.params['sslkey_file'],
        module.params['sslkey_pass']
      )

    return k
    
