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
    groups = k.groups()

    for group in groups:
        if name == group.name:
            return group

    return None


def set_group_send_as(group, users):
    _sendas = group.send_as()
    for sendas in _sendas:
        group.remove_send_as(sendas)

    for sendas in users:
        user = k.get_user(sendas)
        if user is not None:
            group.add_send_as(user)

    return


def set_group_members(group, users):
    _members = group.members(False, True)
    for member in _members:
        group.remove_user(member)

    for member in users:
        user = k.get_user(member)
        if user is not None:
            group.add_user(user)

    return


def run_module():
    global k

    argument_spec = kopano_common_argument_spec()
    argument_spec.update(
        name=dict(type='str', required=True),
        fullname=dict(type='str', required=False, default=''),
        email=dict(type='str', required=False, default=''),
        hidden=dict(type='bool', default=False),
        state=dict(type='str', default='present'),
        members=dict(type='list', required=False, default=[]),
        send_as=dict(type='list', required=False, default=[]),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

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

        else:
            if state == "absent":
                k.remove_group(g.name)
                module.exit_json(
                  changed=True, msg="The group {0} was deleted.".format(name))

        g = k.group(name)

        if len(members):
            set_group_members(g, members)

        if len(send_as):
            set_group_send_as(g, send_as)

        module.exit_json(
            changed=True, msg="The group {0} was created.".format(name))

    except Exception as excep:
        module.fail_json(msg='Kopano error: %s' % to_native(excep))


def main():
    run_module()


if __name__ == '__main__':
    main()
