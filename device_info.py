#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
----------------------------------------------------------------------
Created Date: 58h April 2022
Author: Dennis Cruceru
License: Cisco Sample Code License, Version 1.1
----------------------------------------------------------------------

Copyright (c) 2022 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the 'License'). You may obtain a copy of the
License at
 'https://developer.cisco.com/docs/licenses'
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an 'AS IS'
BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

----------------------------------------------------------------------
"""

# DevNet IR1835 Reservable sandbox
# https://devnetsandbox.cisco.com/RM/Diagram/Index/76ea43fd-1018-478f-840b-fee490179819?diagramType=Topology
ir1835 = {
             "host": "10.10.20.82",
             "username": "developer",
             "password": "C1sco12345",
             "http_port": 443,
             "netconf_port": 830,
             "ssh_port": 22
         }

# DevNet IR8140H Reservable sandbox
# https://devnetsandbox.cisco.com/RM/Diagram/Index/971e8960-6d10-4ea2-a62c-0ad70cef244b?diagramType=Topology
ir8140 = {
             "host": "10.10.20.82",
             "username": "developer",
             "password": "C1sco12345",
             "http_port": 443,
             "netconf_port": 830,
             "ssh_port": 22
         }

# DevNet IOS XE on CSR Always-On sandbox
# https://devnetsandbox.cisco.com/RM/Diagram/Index/27d9747a-db48-4565-8d44-df318fce37ad?diagramType=Topology
ios_xe = {
             "host": "sandbox-iosxe-recomm-1.cisco.com",
             "username": "developer",
             "password": "C1sco12345",
             "http_port": 443,
             "netconf_port": 830,
             "ssh_port": 22
         }   
