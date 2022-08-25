#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Hugues Lepesant <hugues@lepesant.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '0.2',
    'status': ['preview'],
    'supported_by': 'hlepesant'
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
  hlepesant.kopano.kopano_db_user:
    name: john
    password: ahTon1ohYo8u
    email: john.doe@zarafa.com
    fullname: John Doe
    administrator: false
    state: present

- name: Create Kopano User and overwrite quota
  hlepesant.kopano.kopano_db_user:
    name: axel
    password: ahTon1erTo8u
    email: axel.doe@zarafa.com
    fullname: Axel Doe
    administrator: false
    quota_use_default: false
    quota_hard: 200 mb
    state: present

- name: Create Kopano User and overwrite and set all quota
  hlepesant.kopano.kopano_db_user:
    name: axel
    password: ahTon1erTo8u
    email: axel.doe@zarafa.com
    fullname: Axel Doe
    administrator: false
    quota_use_default: false
    quota_hard: 200 mb
    quota_soft: 195 mb
    quota_warn: 190 mb
    state: present
'''

RETURN = '''#'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native

from ansible_collections.hlepesant.kopano.plugins.module_utils.kopano_common import (
    missing_required_lib,
    kopano_found,
    E_IMP_ERR,
    kopano_common_argument_spec,
    KopanoHelpers,
    NotFoundError
)

from kopano.utils import (
    bytes_to_human,
    human_to_bytes
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

# Quotas
def db_user_quota(user, quota_use_default, quota_hard, quota_soft = None, quota_warn = None):

    _change = False
    soft_factor = 0.95
    warn_factor = 0.90

    if user.quota.use_default and quota_use_default:
        _change = False

    if not user.quota.use_default and quota_use_default:
        user.quota.update(
            use_default = True
        )
        _change = True

    if not quota_use_default:
        # hard quota (must be defined)
        quota_hard_b = human_to_bytes(quota_hard)

        # soft quota
        if quota_soft is None:
            quota_soft = bytes_to_human(quota_hard_b * soft_factor)
     
        quota_soft_b = human_to_bytes(quota_soft)

        # warning quota
        if quota_warn is None:
            quota_warn = bytes_to_human(quota_hard_b * warn_factor)
    
        quota_warn_b = human_to_bytes(quota_warn)
        
        if quota_hard_b != user.quota.hard_limit or quota_soft_b != user.quota.soft_limit or quota_warn_b != user.quota.warning_limit:
        
            user.quota.update(
                use_default   = False,
                warning_limit = quota_warn_b,
                soft_limit    = quota_soft_b,
                hard_limit    = quota_hard_b,
            )
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
        quota_use_default=dict(type='bool', required=False, default=True),
        quota_hard=dict(type='str', required=False, default=None),
        quota_soft=dict(type='str', required=False, default=None),
        quota_warn=dict(type='str', required=False, default=None),
        state=dict(type='str', required=False, default='present'),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=[('quota_use_default', False, ['quota_hard'])],
        # required_together=[('quota_soft', 'quota_warn'])],
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
    quota_use_default = module.params['quota_use_default']
    quota_hard = module.params['quota_hard']
    quota_soft = module.params['quota_soft']
    quota_warn = module.params['quota_warn']
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

            # quotas
            quota_changed = False
            quota_changed = db_user_quota(_user, quota_use_default, quota_hard, quota_soft, quota_warn)

            if quota_changed:
                result['message'] += "Quota configuration for user {0} has changed.".format(name)
                result['changed'] = True

            
        module.exit_json(**result)
    
    except Exception as excep:
        module.fail_json(msg='Kopano error: %s' % to_native(excep))


def main():
    run_module()

if __name__ == '__main__':
    main()
