.. _hlepesant.kopano.db_user_module:


**************************
hlepesant.kopano.db_user
**************************

**Create a user**


.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Users management with DB plugin



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3.6
- python3-kopano >= 8.7.0


Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
        <tr>
            <td colspan="1">
                <div class="ansibleOptionAnchor" id="parameter-"></div>
                <b>server_socket</b>
                <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                <div style="font-size: small">
                    <span style="color: purple">string</span>
                </div>
            </td>
            <td>
            </td>
            <td>
              <div>Python-kopano will first look at the provided arguments to determine how and where to connect.</div>
              <div>If there are no such arguments, it will try to get useful settings from /etc/kopano/admin.cfg.</div>
              <div>If this also doesn’t exist, it will fall-back to the default UNIX socket.</div>
            </td>
        </tr>
        <tr>
            <td colspan="1">
                <div class="ansibleOptionAnchor" id="parameter-"></div>
                <b>sslkey_file</b>
                <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                <div style="font-size: small">
                    <span style="color: purple">path</span>
                </div>
            </td>
            <td>
            </td>
            <td>
                <div>Path to the certificate file.</div>
            </td>
        </tr>
        <tr>
            <td colspan="1">
                <div class="ansibleOptionAnchor" id="parameter-"></div>
                <b>sslkey_pass</b>
                <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                <div style="font-size: small">
                    <span style="color: purple">string</span>
                </div>
            </td>
            <td>
            </td>
            <td>
                    <div>The password used while creating the certificate.</div>
            </td>
        </tr>

        <tr>
            <td colspan="1">
                <div class="ansibleOptionAnchor" id="parameter-"></div>
                <b>name</b>
                <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                <div style="font-size: small">
                    <span style="color: purple">string</span>
                     / <span style="color: red">required</span>
                </div>
            </td>
            <td>
            </td>
            <td>
                    <div>The name of the user. With this name the user will log on to the store.</div>
            </td>
        </tr>
        <tr>
            <td colspan="1">
                <div class="ansibleOptionAnchor" id="parameter-"></div>
                <b>email</b>
                <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                <div style="font-size: small">
                    <span style="color: purple">string</span>
                     / <span style="color: red">required</span>
                </div>
            </td>
            <td>
            </td>
            <td>
                    <div>The email address of the user.</div>
            </td>
        </tr>
        <tr>
            <td colspan="1">
                <div class="ansibleOptionAnchor" id="parameter-"></div>
                <b>password</b>
                <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                <div style="font-size: small">
                    <span style="color: purple">string</span>
                     / <span style="color: red">required</span>
                </div>
            </td>
            <td>
            </td>
            <td>
                    <div>The password in plain text. The password will be stored encrypted in the database..</div>
            </td>
        </tr>
        <tr>
            <td colspan="1">
                <div class="ansibleOptionAnchor" id="parameter-"></div>
                <b>fullname</b>
                <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                <div style="font-size: small">
                    <span style="color: purple">string</span>
                     / <span style="color: red">required</span>
                </div>
            </td>
            <td>
            </td>
            <td>
                    <div>The full name of the user.</div>
            </td>
        </tr>
        <tr>
            <td colspan="1">
                <div class="ansibleOptionAnchor" id="parameter-"></div>
                <b>company</b>
                <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                <div style="font-size: small">
                    <span style="color: purple">string</span>
                </div>
            </td>
            <td>
            </td>
            <td>
                    <div>The company the user belong to.</div>
            </td>
        </tr>
        <tr>
            <td colspan="1">
                <div class="ansibleOptionAnchor" id="parameter-"></div>
                <b>administrator</b>
                <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                <div style="font-size: small">
                    <span style="color: purple">boolean</span>
                </div>
            </td>
            <td>
                    <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                <li><div style="color: blue"><b>False</b>&nbsp;&larr;</div></li>
                                <li>True</li>
                    </ul>
            </td>
            <td>
                    <div>When a user is administrator, the user will be allowed to open all Kopano stores of any user.</div>
            </td>
        </tr>
        <tr>
            <td colspan="1">
                <div class="ansibleOptionAnchor" id="parameter-"></div>
                <b>update_password</b>
                <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                <div style="font-size: small">
                    <span style="color: purple">boolean</span>
                </div>
            </td>
            <td>
                    <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                <li><div style="color: blue"><b>False</b>&nbsp;&larr;</div></li>
                                <li>True</li>
                    </ul>
            </td>
            <td>
                    <div>Force password update.</div>
            </td>
        </tr>
        <tr>
            <td colspan="1">
                <div class="ansibleOptionAnchor" id="parameter-"></div>
                <b>send_as</b>
                <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                <div style="font-size: small">
                    <span style="color: purple">list</span>
                </div>
            </td>
            <td>
            </td>
            <td>
                    <div>Add a user to the list of the delegate being updated as a ‘send as’ user.</div>
            </td>
        </tr>
        <tr>
            <td colspan="1">
                <div class="ansibleOptionAnchor" id="parameter-"></div>
                <b>quota_use_default</b>
                <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                <div style="font-size: small">
                    <span style="color: purple">boolean</span>
                </div>
            </td>
            <td>
                    <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                <li><div style="color: blue"><b>True</b>&nbsp;&larr;</div></li>
                                <li>False</li>
                    </ul>
            </td>
            <td>
                    <div>Overwrite default quota.</div>
            </td>
        </tr>
        <tr>
            <td colspan="1">
                <div class="ansibleOptionAnchor" id="parameter-"></div>
                <b>quota_hard</b>
                <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                <div style="font-size: small">
                    <span style="color: purple">string</span>
                </div>
            </td>
            <td>
            </td>
            <td>
                    <div>Quota Hard level. In 'b', 'kb', 'mb', 'gb', 'tb', 'pb'.</div>
            </td>
        </tr>
        <tr>
            <td colspan="1">
                <div class="ansibleOptionAnchor" id="parameter-"></div>
                <b>quota_soft</b>
                <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                <div style="font-size: small">
                    <span style="color: purple">string</span>
                </div>
            </td>
            <td>
            </td>
            <td>
                    <div>Quota Soft level. In 'b', 'kb', 'mb', 'gb', 'tb', 'pb'.<br />
                    Must be lower than quota_hard.<br />
                    If not defined, will be evaluate to 95% of quota_hard.
                    </div>
            </td>
        </tr>
        <tr>
            <td>
                <div class="ansibleOptionAnchor" id="parameter-"></div>
                <b>state</b>
                <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                <div style="font-size: small">
                    <span style="color: purple">string</span>
                </div>
            </td>
            <td>
                    <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                <li><div style="color: blue"><b>present</b>&nbsp;&larr;</div></li>
                                <li>absent</li>
                    </ul>
            </td>
            <td>
                    <div>Specifies the state of the user.</div>
            </td>
        </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - This module supports the DB plugin only.
   - `Users management with DB plugin <https://documentation.kopano.io/kopanocore_administrator_manual/user_management.html#users-management-with-db-plugin>`_



Examples
--------

.. code-block:: yaml

    - name: create a user
      hlepesant.kopano.db_user:
        name: john
        email: john@zarafa.com
        fullname: John Doe
        state: present
        password: MySecretPassword


Return Values
-------------


Status
------


Authors
~~~~~~~

- Hugues Lepesant (@hlepesant)
