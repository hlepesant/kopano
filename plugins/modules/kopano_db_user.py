#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Hugues Lepesant <hugues@lepesant.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '0.2',
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
    name: john
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

# Send AS
def db_user_send_as(user, target):
    _change = False
    _sendas = user.send_as()
    sa = []
    for sendas in _sendas:
       sa.append(sendas.name)

    sa.sort()
    target.sort()

    to_remove = list(set(sa) - set(target))
    to_add = list(set(target) - set(sa))

    for username in to_remove:
        _user = k.get_user(username)
        if _user is not None:
            user.remove_send_as(_user)
            _change = True

    for username in to_add:
        _user = k.get_user(username)
        if _user is not None:
            user.add_send_as(_user)
            _change = True

    return _change


def run_module():
    global k

    argument_spec = kopano_common_argument_spec()
    argument_spec.update(
        name=dict(type='str', required=True),
        email=dict(type='str', required=True),
        password=dict(type='str', required=True, no_log=True),
        company=dict(type='str', required=False, default=None),
        fullname=dict(type='str', required=True),
        administrator=dict(type='bool', required=False, default=False),
        update_password=dict(type='bool', required=False, default=False, no_log=True),
        send_as=dict(type='list', required=False, default=[]),
        state=dict(type='str', required=False, default='present'),
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
        module.fail_json(msg=missing_required_lib('kopano'), exception=E_IMP_ERR)
    
    name = module.params['name']
    email = module.params['email']
    password = module.params['password']
    company = module.params['company']
    fullname = module.params['fullname']
    administrator = module.params['administrator']
    update_password = module.params['update_password']
    send_as = module.params['send_as']
    state = module.params['state']

    _admin_level = 0
    _company = None

    try:
        kopano = KopanoHelpers(module)
        k = kopano.connect()

        if k.multitenant and company is not None:
            _company = k.get_company(company)
        
        if k.multitenant and administrator:
            _admin_level = 1
        
        _user = k.get_user(name)
        
        if _user is None:
            if state == 'present':
                k.create_user(name, email, password, _company, fullname, True)
                result['changed'] = True
                result['message'] = "The user {0} was created.".format(name)
            else:
                result['changed'] = False
                result['message'] = "The user {0} does not exists.".format(name)
        
            module.exit_json(**result)

        # user found
        if state == 'absent':
            k.remove_user(_user)
            result['changed'] = True
            result['message'] = "The user {0} was deleted.".format(name)
        
        else:
        
            if _user.email != email:
                _user.email = email
                result['changed'] = True
                result['message'] += "The email for user {0} was udpated.".format(name)
            
            if _user.fullname != fullname:
                _user.fullname = fullname
                result['changed'] = True
                result['message'] += "The fullname for user {0} was udpated.".format(name)
            
            if update_password:
                _user.password = password
                result['changed'] = True
                result['message'] += "The password for user {0} was udpated.".format(name)

            if( db_user_send_as(_user, send_as) ):
                result['message'] += "SendAs of user {0} has changed.".format(name)
                result['changed'] = True
            
        module.exit_json(**result)
    
    except Exception as excep:
        module.fail_json(msg='Kopano error: %s' % to_native(excep))


def main():
    run_module()

if __name__ == '__main__':
    main()
