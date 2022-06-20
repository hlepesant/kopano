#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Hugues Lepesant <hugues@lepesant.com>
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

short_description: Create a kopano user

description:
  - Create a kopano user

References : 
  - https://documentation.kopano.io/kopanocore_administrator_manual/user_management.html#users-management-with-db-plugin

author: Hugues Lepesant (@hlepesant)
version: 0.1
options:

'''

EXAMPLES = r'''
- name: Create Kopano User
  community.kopano.kopano_db_user:
    username: john
    password: ahTon1ohYo8u
    email: john.doe@zarafa.com
    fullname: John Doe
    administrator: false
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
    username=dict(type='str', required=True),
    password=dict(type='str', required=True, no_log=True),
    email=dict(type='str', required=True),
    fullname=dict(type='str', required=True),
    administrator=dict(type='bool', required=False, default=False),
    state=dict(type='str', default='present'),
  )

  module = AnsibleModule(
    argument_spec=argument_spec,
    supports_check_mode=True,
  )

  if not kopano_found:
    module.fail_json(msg=missing_required_lib('kopano'),
      exception=E_IMP_ERR)

  username = module.params['username']
  password = module.params['password']
  email = module.params['email']
  fullname = module.params['fullname']
  administrator = module.params['administrator']
  state = module.params['state']
  create_store = True

  try:
    kopano = KopanoHelpers(module)
    k = kopano.connect()

    if not k.multitenant:
      _admin_level = 0
    else:
      if administrator:
        _admin_level = 1
      else:
        _admin_level = 0

    _user = k.get_user(username)

    if _user is None:
      if state == 'present':
        k.create_user(username, email, password, None, fullname, create_store)
        module.exit_json(changed=True, msg="The user {0} was created.".format(username))
      else:
        module.exit_json(changed=False, msg="The user {0} does not exists.".format(username))
    else:
      if state == 'absent':
        # k.delete(_user)
        k.remove_user(_user)
        module.exit_json(changed=True, msg="The user {0} was deleted.".format(username))
      else:
        module.exit_json(changed=False, msg="The user {0} already exists.".format(username))

  except Exception as excep:
    module.fail_json(msg='Kopano error: %s' % to_native(excep))


def main():
    run_module()

if __name__ == '__main__':
    main()
