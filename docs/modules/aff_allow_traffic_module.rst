.. _aff_allow_traffic:


aff_allow_traffic
+++++++++++++++++

.. versionadded:: 0.1


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Check and create traffic change requests with Algosec FireFlow.
* Algosec Ansible module will help you manage and orchestrate your tasks to work with Algosec FireFlow service. When used, the `aff` command will check if a certain traffic is allowed between `source` and `dest`. If the connectivity is not allowed between the nodes, the module will create a "Change Request" on Algosec's FireFlow and will provide the change request url in the module call result.


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
           <td>requester<br/>
               <div style="font-size: small;"></div>
           </td>
           <td>yes</td>
           <td></td>
           <td></td>
           <td>
               <div>The first and last name of the requester.</div>
           </td>
       </tr>
      <tr>
           <td>email<br/>
               <div style="font-size: small;"></div>
           </td>
           <td>yes</td>
           <td></td>
           <td></td>
           <td>
               <div>The email address of the requester.</div>
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
               <div>Comma separated list of IP address for the traffic sources.</div>
           </td>
       </tr>
      <tr>
           <td>destination<br/>
               <div style="font-size: small;"></div>
           </td>
           <td>yes</td>
           <td></td>
           <td></td>
           <td>
               <div>Comma separated list of IP address for the traffic destinations.</div>
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
               List of services of the traffic to allow. Accepted services are as defined on Algosec or by port/proto format
               (e.g. tcp/50,udp/100,ssh).
               </div>
           </td>
       </tr>
      <tr>
           <td>transport<br/>
               <div style="font-size: small;"></div>
           </td>
           <td>no</td>
           <td>ipv4</td>
           <td>ipv4,ipv6</td>
           <td>
               <div>IP version of the traffic to allow</div>
           </td>
       </tr>

   </table>
   </br>



Examples
--------

 ::

   - name: Create Traffic Change Request if needed
     hosts: algosec-server

     - name: Create Traffic Change Request
       # We use delegation to use the local python interpreter (and virtualenv if enabled)
       delegate_to: localhost
       aff_allow_traffic:
         ip_address: 192.168.58.128
         user: admin
         password: S0mePA$$w0rd

         requester: almogco
         email: almog@email.com
         sources: 192.168.12.12,123.123.132.123
         destinations: 16.47.71.62,234.234.234.234
         services: HTTPS,http,tcp/80,tcp/51
       register: result

     - name: Print the test results
       debug: var=result

Return Values
-------------

The following are the fields unique to this module:

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
           <td> connectivity_status</td>
           <td> The current connectivity status of the traffic. Can be Allowed, Blocked, Partially Blocked or Not Routed.</td>
           <td align=center> always</td>
           <td align=center> string</td>
           <td align=center> Allowed</td>
       </tr>
       <tr>
           <td> is_traffic_allowed</td>
           <td> State whether the traffic is currently allowed.</td>
           <td align=center> always</td>
           <td align=center> bool</td>
           <td align=center> true</td>
       </tr>
       <tr>
           <td> change_request_url</td>
           <td> URL for the change request ticket on the Algosec server.</td>
           <td align=center> success</td>
           <td align=center> string</td>
           <td align=center> https://192.168.58.128/FireFlow/Ticket/Display.html?id=4447</td>
       </tr>
   </table>
   </br></br>

