.. _abf_update_flow:


abf_update_flow
+++++++++++++++

.. versionadded:: 0.1


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Create new Application Flows on Algosec Business Flow.
* If the requested flow is a subset of one of the flows of the relevant Application, flow creation is cancelled.


Requirements (on host that executes module)
-------------------------------------------

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
               <div>IP address (or hostname) of the Algosec server.</div>
           </td>
       </tr>
       <tr>
           <td>user<br/>
               <div style="font-size: small;"></div>
           </td>
           <td>yes</td>
           <td>admin</td>
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
           <td>app_name<br/>
               <div style="font-size: small;"></div>
           </td>
           <td>yes</td>
           <td></td>
           <td></td>
           <td>
               <div>BusinessFlow Application to add the flow to.</div>
           </td>
       </tr>
       <tr>
           <td>name<br/>
               <div style="font-size: small;"></div>
           </td>
           <td>no</td>
           <td></td>
           <td></td>
           <td>
               <div>Name for the flow to be created</div>
           </td>
       </tr>
       <tr>
           <td>sources<br/>
               <div style="font-size: small;"></div>
           </td>
           <td>yes</td>
           <td></td>
           <td></td>
           <td>
               <div>Comma separated list of IPs or ABF network objects of traffic sources for the flow</div>
           </td>
       </tr>
       <tr>
           <td>destinations<br/>
               <div style="font-size: small;"></div>
           </td>
           <td>yes</td>
           <td></td>
           <td></td>
           <td>
               <div>Comma separated list of IPs or ABF network objects of traffic destinations for the flow</div>
           </td>
       </tr>
       <tr>
           <td>services<br/>
               <div style="font-size: small;"></div>
           </td>
           <td>yes</td>
           <td></td>
           <td></td>
           <td>
               <div>
                    Comma separated list of traffic services to allow in the flow. Services can be as defined on Algosec
                    BusinessFlow or in a proto/port format (only UDP and TCP are supported as proto. e.g. tcp/50).
               </div>
           </td>
       </tr>
       <tr>
           <td>users<br/>
               <div style="font-size: small;"></div>
           </td>
           <td>no</td>
           <td></td>
           <td></td>
           <td>
               <div>Comma separated list of users the flow is relevant to.</div>
           </td>
       </tr>
       <tr>
           <td>network_applications<br/>
               <div style="font-size: small;"></div>
           </td>
           <td>no</td>
           <td></td>
           <td></td>
           <td>
               <div>Comma separated list of network application names the flow is relevant to.</div>
           </td>
       </tr>
       <tr>
           <td>comment<br/>
               <div style="font-size: small;"></div>
           </td>
           <td>no</td>
           <td>Flow created by AlgosecAnsible</td>
           <td></td>
           <td>
               <div>Comment to attach to the flow</div>
           </td>
       </tr>
       <tr>
           <td>apply_draft<br/>
               <div style="font-size: small;"></div>
           </td>
           <td>no</td>
           <td>True</td>
           <td></td>
           <td>
               <div>
            Apply the AlgoSec BusinessFlow application draft. Applying the application draft should be done after every batch of flow updates as each draft application may take a few minutes to execute. If you have more than one abf_flow_update module usage in your ansible playbook, it is recommended to set the "apply_draft" to False to all module calls but the last one (that should be True). Make sure that this module is called with "apply_draft" set to True at the last time it is used in an
            Ansible playbook.
               </div>
           </td>
       </tr>
    apply_draft:
        default: True
        description:
            -
   </table>
   </br>



Examples
--------

 ::

   - name: Create a flow on an AlsogsecBusinessFlow App
     hosts: algosec-server

     tasks:
     - name: Create the flow on ABF
       # We use delegation to use the local python interpreter (and virtualenv if enabled)
       delegate_to: localhost
       abf_update_flow:
         ip_address: 192.168.58.128
         user: admin
         password: S0mePA$$w0rd

         app_name: Payroll
         name: payroll-server-auth
         sources: 192.168.12.12
         destinations: 16.47.71.62,16.47.71.63
         services: HTTPS,tcp/23
