# Kopano Collection for Ansible

Documentation for the collection.

Managed Kopano's object, when server is  configured to use the [The DB Authentication Plugin](https://documentation.kopano.io/kopanocore_administrator_manual/configure_kc_components.html#the-db-authentication-plugin).  

## Code of Conduct

We follow the [Ansible Code of Conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html) in all our interactions within this project.

If you encounter abusive behavior violating the [Ansible Code of Conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html), please refer to the [policy violations](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html#policy-violations) section of the Code of Conduct for information on how to raise a complaint.

## Contributing

The content of this collection is made by [people](https://github.com/hlepesant/kopano/blob/main/CONTRIBUTORS) just like you, a community of individuals collaborating on making the world better through developing automation software.

We are actively accepting new contributors.

Any kind of contribution is very welcome.

You don't know how to start? Refer to our [contribution guide](https://github.com/hlepesant/kopano/blob/main/CONTRIBUTING.md)!

## Collection maintenance

The current maintainers (contributors with `write` or higher access) are listed in the [MAINTAINERS](https://github.com/hlepesant/kopano/blob/main/MAINTAINERS) file. If you have questions or need help, feel free to mention them in the proposals.

To learn how to maintain / become a maintainer of this collection, refer to the [Maintainer guidelines](https://github.com/hlepesant/kopano/blob/main/MAINTAINING.md).

It is necessary for maintainers of this collection to be subscribed to:

* The collection itself (the `Watch` button -> `All Activity` in the upper right corner of the repository's homepage).
* The "Changes Impacting Collection Contributors and Maintainers" [issue](https://github.com/hlepesant/kopano/issues).

They also should be subscribed to Ansible's [The Bullhorn newsletter](https://docs.ansible.com/ansible/devel/community/communication.html#the-bullhorn).

## Communication

Have a look to [CHANGELOG](https://github.com/hlepesant/kopano/blob/main/CHAGELOG.md).

For more information about communication, refer to the [Ansible Communication guide](https://docs.ansible.com/ansible/devel/community/communication.html).

## Governance

The process of decision making in this collection is based on discussing and finding consensus among participants.

Every voice is important and every idea is valuable. If you have something on your mind, create an issue or dedicated discussion and let's discuss it!

## Included content

- **Modules**:
  - [kopano_public_store](https://github.com/hlepesant/kopano/blob/main/docs/hlepesant.kopano.public_store_module.rst)
  - [kopano_company](https://github.com/hlepesant/kopano/blob/main/docs/hlepesant.kopano.company.rst)
  - [kopano_db_user](https://github.com/hlepesant/kopano/blob/main/docs/hlepesant.kopano.db.user.rst)
  - [kopano_db_group](https://github.com/hlepesant/kopano/blob/main/docs/hlepesant.kopano.db.group.rst)


## Tested with

### ansible-core

- 2.12

### Kopano Server

- kopano 8.7.0 on Debian 10 Buster

## External requirements

The Kopano modules rely on a [python3-kopano](https://packages.debian.org/buster/python3-kopano).

## Using this collection

### Installing the Collection from Ansible Galaxy

Before using the Kopano collection, you need to install it with the Ansible Galaxy CLI:

```bash
ansible-galaxy collection install hlepesant.kopano
```

You can also include it in a `requirements.yml` file and install it via `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: hlepesant.kopano
```

Note that if you install the collection from Ansible Galaxy, it will not be upgraded automatically if you upgrade the Ansible package. To upgrade the collection to the latest available version, run the following command:

```bash
ansible-galaxy collection install hlepesant.kopano --upgrade
```

You can also install a specific version of the collection, for example, if you need to downgrade when something is broken in the latest version (please report an issue in this repository). Use the following syntax:

```bash
ansible-galaxy collection install hlepesant.kopano:==0.0.2
```

See [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Licensing

<!-- Include the appropriate license information here and a pointer to the full licensing details. If the collection contains modules migrated from the ansible/ansible repo, you must use the same license that existed in the ansible/ansible repo. See the GNU license example below. -->

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.


