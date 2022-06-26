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
module: kopano_public_store

short_description: Create a kopano public store

description:
  - Create a kopano public store

references: 
  - https://documentation.kopano.io/kopanocore_administrator_manual/user_management.html#public-folder

author: Hugues Lepesant (@hlepesant)
version_
options:

'''

EXAMPLES = r'''
- name: Create Kopano public store
  community.kopano.kopano_public_store:
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
        state=dict(type='str', default='present'),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    result = dict(
        changed=False,
        original_message='',
        message=''
    )
    result['original_message'] = module.params['name']
    result['message'] = ""

    if not kopano_found:
        module.fail_json(msg=missing_required_lib('kopano'),
            exception=E_IMP_ERR)

    try:
        kopano = KopanoHelpers(module)
        k = kopano.connect()
        
        state = module.params['state']
        
        _public_store = k.public_store
        
        if (_public_store is None):
            if state == "present":
                k.create_public_store()
                result['message'] += "The public store was created."
                result['changed'] = True
        else:
            result['message'] += "The public store already exists."
            result['changed'] = False
        
        if state == "absent":
            result['message'] += "The public store can not be deleted."
            result['changed'] = False
    
        module.exit_json(**result)

    except Exception as excep:
        module.fail_json(msg='Kopano error: %s' % to_native(excep))


def main():
    run_module()

if __name__ == '__main__':
    main()
