.. _community.kopano.company_module:


**************************
community.kopano.company
**************************

**Create a company**


.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Create a company.



Requirements
------------
The below requirements are needed on the host that executes this module.

- python >= 3.6
- python3-kopano >= 8.7.0
- Mutli tenant kopano environment.


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
                </div>
            </td>
            <td>
            </td>
            <td>
                    <div>The name of the company.</div>
            </td>
        </tr>
        <tr>
            <td>
                <div class="ansibleOptionAnchor" id="parameter-"></div>
                <b>state</b>
                <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                <div style="font-size: small">
                    <span style="color: purple">string</span>
                     / <span style="color: red">required</span>
                </div>
            </td>
            <td>
                    <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                <li><div style="color: blue"><b>present</b>&nbsp;&larr;</div></li>
                                <li>absent</li>
                    </ul>
            </td>
            <td>
                    <div>Specifies the state of the company.</div>
            </td>
        </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Company need a multi tenant configuration. So be sure to have set `enable_hosted_kopano = true`.



Examples
--------

.. code-block:: yaml

    - name: create a company
      community.kopano.company:
        name: Zarafa
        state: present


Return Values
-------------


Status
------


Authors
~~~~~~~

- Hugues Lepesant (@hlepesant)
