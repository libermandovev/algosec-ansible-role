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
* No change request is created if traffic is already provisioned correctly.


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
           <td>traffic_lines<br/>
               <div style="font-size: small;"></div>
           </td>
           <td>yes</td>
           <td></td>
           <td></td>
           <td>
               <div>
                  List of dictionaries, each define a traffic lines that should be added into the change request. Each traffic_line dict object should contain the following keys: <b>action</b>, <b>sources</b>, <b>destinations</b>and <b>services</b>.
                  <br>
                    <ul>
                        <li>
                            <b>action</b> - Boolean. True to allow traffic or False to drop it.
                        </li>
                        <li>
                            <b>sources</b> - list of IP addresses or BusinessFlow objects
                        </li>
                        <li>
                            <b>destinations</b> - list of IP addresses or BusinessFlow objects
                        </li>
                        <li>
                            <b>services</b> - list of services of the traffic to allow. Accepted services are as defined on AlgoSec BusinessFlow or by port/proto format (e.g. tcp/50,udp/100,ssh).
                        </li>
                    </ul>
                  Please usage examples in the `Examples`_ section.
               </div>
           </td>
       </tr>
      <tr>
           <td>template<br/>
               <div style="font-size: small;"></div>
           </td>
           <td>no</td>
           <td>None</td>
           <td></td>
           <td>
               <div>Full name of the template to use for the newly created change request.</div>
           </td>
       </tr>
   </table>
   </br>



Examples
--------

.. include:: ../../examples/algosec_provision_network_connectivity.yml
    :literal:

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
           <td align=center> https://local.algosec.com/FireFlow/Ticket/Display.html?id=4447</td>
       </tr>
   </table>
   </br></br>

