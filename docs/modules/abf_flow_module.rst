.. _abf_flow:


abf_flow
+++++++++

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
               <div>Comma separated IP list of traffic sources for the flow</div>
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
               <div>Comma separated IP list of traffic destinations for the flow</div>
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
       abf_flow:
         ip_address: 192.168.58.128
         user: admin
         password: S0mePA$$w0rd

         app_name: Payroll
         name: payroll-server-auth
         sources: 192.168.12.12
         destinations: 16.47.71.62,16.47.71.63
         services: HTTPS,tcp/23
