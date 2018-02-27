.. _algosec_provision_network_connectivity:


algosec_provision_network_connectivity
++++++++++++++++++++++++++++++++++++++

.. versionadded:: 0.1.0


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Provision network connectivity by creating a change request in AlgoSec FireFlow.
* No change request is created if traffic is already allowed.


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
           <td>True</td>
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
           <td>requestor<br/>
               <div style="font-size: small;"></div>
           </td>
           <td>yes</td>
           <td></td>
           <td></td>
           <td>
               <div>The first and last name of the requestor.</div>
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
               <div>The email address of the requestor.</div>
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
               List of services of the traffic to allow. Accepted services are as defined on AlgoSec or by port/proto format
               (e.g. tcp/50,udp/100,ssh).
               </div>
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
       algosec_provision_network_connectivity:
         ip_address: 192.168.58.128
         user: admin
         password: S0mePA$$w0rd

         requestor: almogco
         email: almog@email.com
         sources: 192.168.12.12,123.123.132.123
         destinations: 16.47.71.62,234.234.234.234
         services: HTTPS,http,tcp/80,tcp/51
       register: result

     - name: Print the test results
       debug: var=result

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
           <td> change_request_url</td>
           <td> URL for the change request ticket on the AlgoSec server.</td>
           <td align=center> success</td>
           <td align=center> string</td>
           <td align=center> https://192.168.58.128/FireFlow/Ticket/Display.html?id=4447</td>
       </tr>
   </table>
   </br></br>

