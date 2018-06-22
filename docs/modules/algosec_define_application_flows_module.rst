.. _algosec_define_application_flows:


algosec_define_application_flows
++++++++++++++++++++++++++++++++

.. versionadded:: 0.3.0


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Update application flows of an AlgoSec BusinessFlow application to match a requested configuration.
* Create, modify or delete application flows if needed.
* Apply the changes in BusinessFlow to automatically create a FireFlow change request.
* Optionally make sure that all defined flow pass the flow connectivity check on BusinessFlow


Requirements
------------

  * `algosec` can be obtained from PyPi https://pypi.python.org/pypi/algosec


Options
-------

.. raw:: html

    <table border=1 cellpadding=4>
       <tr>
           <th class="head">parameter</th>
           <th class="head">required</th>
           <th class="head">default</th>
           <th class="head">choices</th>
           <th class="head">comments</th>
       </tr>
       <tr>
           <td>ip_address<br/>
               <div style="font-size: small;"></div>
           </td>
           <td>yes</td>
           <td></td>
           <td></td>
           <td>
               <div>IP address (or hostname) of the AlgoSec server.</div>
           </td>
       </tr>
       <tr>
           <td>user<br/>
               <div style="font-size: small;"></div>
           </td>
           <td>yes</td>
           <td></td>
           <td></td>
           <td>
               <div>Username credentials to use for auth.</div>
           </td>
       </tr>
       <tr>
           <td>password<br/>
               <div style="font-size: small;"></div>
           </td>
           <td>yes</td>
           <td></td>
           <td></td>
           <td>
               <div>Password credentials to use for auth.</div>
           </td>
       </tr>
       <tr>
           <td>certify_ssl<br/>
               <div style="font-size: small;"></div>
           </td>
           <td>no</td>
           <td>False</td>
           <td></td>
           <td>
               <div>
                  Set whether or not to validate the AlgoSec server SSL certificate.
                  This flag might be set to False only in testing environments.
                  It is highly unrecommended to set it to False in production environments.
               </div>
           </td>
       </tr>
       <tr>
           <td>app_name<br/>
               <div style="font-size: small;"></div>
           </td>
           <td>yes</td>
           <td></td>
           <td></td>
           <td>
               <div>BusinessFlow Application to update.</div>
           </td>
       </tr>
       <tr>
           <td>app_flows<br/>
               <div style="font-size: small;"></div>
           </td>
           <td>yes</td>
           <td></td>
           <td></td>
           <td>
               <div>
                  Full list of application flows to be applied. The configuration can be also provided from a JSON file.
                  Please usage examples in the `Examples`_ section.
               </div>
           </td>
       </tr>
       <tr>
           <td>check_connectivity<br/>
               <div style="font-size: small;"></div>
           </td>
           <td>no</td>
           <td>false</td>
           <td></td>
           <td>
               <div>
                  Assert that all flows pass flow connectivity check on BusinessFlow.
                  If any of the unchanged flows are not passing connectivity test, fail and report their names.
               </div

           </td>
       </tr>
   </table>
   </br>

Return Values
-------------

.. raw:: html

   <table border=1 cellpadding=4>
       <tr>
           <th class="head">name</th>
           <th class="head">description</th>
           <th class="head">returned</th>
           <th class="head">type</th>
           <th class="head">sample</th>
       </tr>
       <tr>
           <td> app_name</td>
           <td> The BusinessFlow application for which flows were defined.</td>
           <td align=center> always</td>
           <td align=center> string</td>
           <td align=center> PayrollApp</td>
       </tr>
       <tr>
           <td> deleted_flows</td>
           <td> Number of flows deleted. </td>
           <td align=center> always</td>
           <td align=center> int</td>
           <td align=center></td>
       </tr>
       <tr>
           <td> created_flows</td>
           <td> Number of flows created. </td>
           <td align=center> always</td>
           <td align=center> int</td>
           <td align=center> </td>
       </tr>
       <tr>
           <td> modified_flows</td>
           <td> Number of flows modified. </td>
           <td align=center> always</td>
           <td align=center> int</td>
           <td align=center> </td>
       </tr>
       <tr>
           <td> unchanged_flows</td>
           <td> Number of flows left unchanged. </td>
           <td align=center> always</td>
           <td align=center> int</td>
           <td align=center> </td>
       </tr>
       <tr>
           <td> blocked_flows</td>
           <td> List of flow names that failed connectivity check.</td>
           <td align=center> only when connectivity check fails, when check_connectivity flag in on.</td>
           <td align=center> list</td>
           <td align=center> ["flow1", "flow2", "flow3"]</td>
       </tr>
   </table>
   </br></br>


Examples
--------

 ::

   - name: Update application flows of an AlgoSec BusinessFlow application
     hosts: algosec-server
     gather_facts: False

     roles:
       - role: algosec.algosec

     tasks:
     - name: Grab AlgoSec credentials from ansible-vault
       include_vars: 'algosec-secrets.yml'
       no_log: 'yes'

     - name: Set App flows on ABF using JSON configuration loaded from file
       # We use delegation to use the local python interpreter (and virtualenv if enabled)
       delegate_to: localhost
       vars:
         flows_data: "{{ lookup('file','vars/application-flows.json')|from_json }}"

       algosec_define_application_flows:
         ip_address: "{{ ip_address }}"
         user: "{{ username }}"
         password: "{{ password }}"
         app_name: "{{ item.app_name}}"
         app_flows: "{{item.app_flows}}"
       with_items: "{{ flows_data.applications }}"


Example For Application Flows JSON File
---------------------------------------

 ::

   {
     "applications": [
       {
         "app_name": "TEST",
         "app_flows": {
           "flow1": {
             "sources": ["HR Payroll server", "192.168.0.0/16"],
             "destinations": ["16.47.71.62"],
             "services": ["HTTPS"]
           },
           "flow2": {
             "sources": ["10.0.0.1"],
             "destinations": ["10.0.0.2"],
             "services": ["udp/501"]
           },
           "flow3": {
             "sources": ["1.2.3.4"],
             "destinations": ["3.4.5.6"],
             "services": ["SSH"]
           }
         }
       },
       {
         "app_name": "ANOTHER-APP",
         "app_flows": {
           "new-flow": {
             "sources": ["1.2.3.4"],
             "destinations": ["3.4.5.6"],
             "services": ["SSH"]
           }
         }
       }
     ]
   }

