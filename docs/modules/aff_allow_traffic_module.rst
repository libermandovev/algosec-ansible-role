.. _aff_allow_traffic:


aff_allow_traffic
+++++++++++++++++

.. versionadded:: 0.1


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Apply an authcode to a device.
* The authcode should have been previously registered on the Palo Alto Networks support portal.
* The device should have Internet access.


Requirements (on host that executes module)
-------------------------------------------

  * pan-python


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

        - hosts: localhost
          connection: local
          tasks:
              - name: Create the FireFlow ticket if traffic not allowed
               aff_allow_traffic:
                  ip_address: "{{ ip_address }}"
                  user: "{{ username }}"
                  password: "{{ password }}"

                  # Specific connectivity check parameters
                  requestor: almogco
                  email: almog@algosec.com
                  sources: 192.168.1.1,192.168.1.2
                  destinations: 8.8.8.8,4.4.4.4
                  services: http,dns
               register: result
        - name: Display the url for the created change request ticket (if already registered)
            - debug: var=result

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

