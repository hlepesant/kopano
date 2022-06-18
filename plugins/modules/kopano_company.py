#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2012, Mark Theunissen <mark.theunissen@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '0.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: kopano_company

short_description: Create a kopano company

description:
  - Create a kopano company

References : 
  - https://documentation.kopano.io/kopanocore_administrator_manual/special_kc_configurations.html#multi-tenancy-configurations

author: Hugues Lepesant (@hlepesant)
version: 0.1
options:

'''

EXAMPLES = r'''
- name: Create Kopano Company
  community.kopano.kopano_company:
    name: Zarafa
    state: present
'''

RETURN = '''#'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native

from ansible_collections.community.kopano.plugins.module_utils.kopano_common import (
    missing_required_lib,
    kopano_found,
    E_IMP_ERR,
    kopano_common_argument_spec,
    KopanoHelpers,
    NotFoundError
)


def run_module():

  argument_spec = kopano_common_argument_spec()
  argument_spec.update(
    name=dict(type='str', required=True),
    state=dict(type='str', default='present'),
  )

  module = AnsibleModule(
    argument_spec=argument_spec,
    supports_check_mode=True,
  )

  if not kopano_found:
    module.fail_json(msg=missing_required_lib('kopano'),
      exception=E_IMP_ERR)

  name = module.params['name']
  state = module.params['state']

  try:
    kopano = KopanoHelpers(module)
    k = kopano.connect()

    if not k.multitenant:
      module.exit_json(changed=False, msg="Unable to create company {0}: action not supported by server in single-tenancy support. ".format(name))

    _company = k.get_company(name)

    if _company is None:
      if state == 'present':
        k.create_company(name)
        module.exit_json(changed=True, msg="The company {0} was created.".format(name))
      else:
        module.exit_json(changed=False, msg="The company {0} do not exists.".format(name))
    else:
      if state == 'absent':
        k.delete(_company)
        module.exit_json(changed=True, msg="The company {0} was deleted.".format(name))
      else:
        module.exit_json(changed=False, msg="The company {0} already exists.".format(name))

  except Exception as excep:
    module.fail_json(msg='Kopano error: %s' % to_native(excep))


def main():
    run_module()

if __name__ == '__main__':
    main()
