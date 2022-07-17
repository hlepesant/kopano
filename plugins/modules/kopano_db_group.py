#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Hugues Lepesant <hugues@lepesant.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function
from ansible_collections.community.kopano.plugins.module_utils.kopano_common import (
    missing_required_lib,
    kopano_found,
    E_IMP_ERR,
    kopano_common_argument_spec,
    KopanoHelpers,
    NotFoundError
)
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '0.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: kopano_db_group

short_description: Create a kopano group

description:
  - Create a kopano group

References :
  - https://documentation.kopano.io/kopanocore_administrator_manual/user_management.html#groups

author: Hugues Lepesant (@hlepesant)
version: 0.1
options:

'''

EXAMPLES = r'''
- name: Create Kopano Group
  community.kopano.kopano_db_group:
    name: support
    email: support@zarafa.com
    members:
      - john
    state: present
'''

RETURN = '''#'''


def get_group(name):
    try:
        group = k.group(name, False)
    except kopano.NotFoundError:
        return None
    return group

def db_group_members(group, target):
    _change = False
    _members = group.users()
    mb = []
    for member in _members:
       mb.append(member.name)

    mb.sort()
    target.sort()

    to_remove = list(set(mb) - set(target))
    to_add = list(set(target) - set(mb))

    for username in to_remove:
        user = k.get_user(username)
        if user is not None:
            group.remove_user(user)
            _change = True

    for username in to_add:
        user = k.get_user(username)
        if user is not None:
            group.add_user(user)
            _change = True

    return _change

def db_group_send_as(group, target):
    _change = False
    _sendas = group.send_as()
    sa = []
    for sendas in _sendas:
       sa.append(sendas.name)

    sa.sort()
    target.sort()

    to_remove = list(set(sa) - set(target))
    to_add = list(set(target) - set(sa))

    for username in to_remove:
        user = k.get_user(username)
        if user is not None:
            group.remove_send_as(user)
            _change = True

    for username in to_add:
        user = k.get_user(username)
        if user is not None:
            group.add_send_as(user)
            _change = True

    return _change

def run_module():
    global k

    argument_spec = kopano_common_argument_spec()
    argument_spec.update(
        name=dict(type='str', required=True),
        fullname=dict(type='str', required=False, default=''),
        email=dict(type='str', required=False, default=''),
        hidden=dict(type='bool', default=False),
        members=dict(type='list', required=False, default=[]),
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
        module.fail_json(msg=missing_required_lib('kopano'),
                         exception=E_IMP_ERR)

    name = module.params['name']
    fullname = module.params['fullname']
    email = module.params['email']
    state = module.params['state']
    hidden = module.params['hidden']
    members = module.params['members']
    send_as = module.params['send_as']

    try:
        kopano = KopanoHelpers(module)
        k = kopano.connect()

        g = get_group(name)

        if g is None:
            if state == "present":
                k.create_group(name, fullname, email, hidden, None)
                result['message'] += "The group {0} was created. ".format(name)
                result['changed'] = True

        if state == "absent":
            k.remove_group(g.name)
            result['message'] = "The group {0} was deleted.".format(name)
            result['changed'] = True
            module.exit_json(**result)

        # we need to refresh the group object
        # g = get_group(name)
        g = k.group(name, False)

        if ( db_group_members(g, members) ):
            result['message'] += "Members of group {0} has changed. ".format(name)
            result['changed'] = True

        if( db_group_send_as(g, send_as) ):
            result['message'] += "SendAs of group {0} has changed.".format(name)
            result['changed'] = True

        module.exit_json(**result)

    except Exception as excep:
        module.fail_json(msg='Kopano error: %s' % to_native(excep))


def main():
    run_module()


if __name__ == '__main__':
    main()
