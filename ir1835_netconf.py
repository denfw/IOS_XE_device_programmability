#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
----------------------------------------------------------------------
Created Date: 8th April 2022
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

from device_info import ir1835
from ncclient import manager
from lxml import etree
import urllib3
import click


@click.group()
def cli():
    """Simple script to perform various tasks on IOS XE devices"""
    pass

@click.command(name="get-request")
@click.argument('xmlstring', type=click.File(mode='r'))
def get_request(xmlstring):
    print("XML FILTER:")
    netconf_filter=xmlstring.read()
    print(netconf_filter)
    print("-" * 80)
    with manager.connect(host=ir1835["host"], port=ir1835["netconf_port"],
                     username=ir1835["username"], password=ir1835["password"],
                     hostkey_verify=False, device_params={},
                     allow_agent=False, look_for_keys=False) as device:
                    
                    netconf_get_reply = device.get(('subtree', netconf_filter))

    print("NETCONF RESPONSE:")
    print(etree.tostring(netconf_get_reply.data_ele, pretty_print=True).decode('utf-8'))
    print("-" * 80)
    

@click.command(name="edit-request")
@click.argument('xmlstring', type=click.File(mode='r'))
def edit_request(xmlstring):
    print("XML CONFIG STRING:")
    netconf_filter = xmlstring.read()
    print(netconf_filter)
    print("-" * 80)
    with manager.connect(host=ir1835["host"], port=ir1835["netconf_port"],
                     username=ir1835["username"], password=ir1835["password"],
                     hostkey_verify=False, device_params={},
                     allow_agent=False, look_for_keys=False) as device:
                    
                    nc_reply = device.edit_config(target='running', config=netconf_filter)
    
    print("NETCONF RESPONSE:")
    print(nc_reply)
    print("-" * 80)

@click.command(name='create-config')
@click.argument('name')
@click.argument('address')
@click.argument('mask')
def create_config_file(name, address, mask):
    nc_config=f"""
        <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
          <interface>
                <name>{name}</name>
                <description>NETCONF test description</description>
                <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:l3ipvlan</type>
                <enabled>true</enabled>
                <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                    <address>
                        <ip>{address}</ip>
                        <netmask>{mask}</netmask>
                    </address>
                </ipv4>
            </interface>
        </interfaces>
    </config>
    """
    file = open("config.xml","w")
    file.write(nc_config)
    file.close()

cli.add_command(get_request)
cli.add_command(edit_request)
cli.add_command(create_config_file)

if __name__ == "__main__":
    cli()
