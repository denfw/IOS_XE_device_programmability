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

from textwrap import indent
from prettytable import PrettyTable
from device_info import ir1835
import requests
import urllib3
import json
import click

# Silence the insecure warning due to SSL Certificate
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Create the generic headers to specify what type of content to send and accept
headers = {
    'Accept': 'application/yang-data+json, application/yang-data.errors+json',
    'Content-type': 'application/yang-data+json'
}


@click.group()
def cli():
    """Simple script to perform various tasks on IOS XE devices using"""
    pass


@click.command(name='get-config')
def get_running_config():
    """
    Retrieve the running configuration
    """
    url = f"https://{ir1835['host']}/restconf/data/Cisco-IOS-XE-native:native"

    click.secho("Retrieving running configuration")
    # Make Login request and return the response body
    response = requests.request(
        "GET", url, auth=(ir1835["username"], ir1835["password"]), headers=headers, verify=False
    )

    # Retrieve the running configuration from the response and format it
    click.echo(json.dumps(response.json(), indent=3))


@click.command(name='get-static')
def get_static_routes():
    """
    Retrieve the statically configured routes
    """
    url = f"https://{ir1835['host']}/restconf/data/ietf-routing:routing/"

    click.secho("Retrieving static routes")
    # Make a request and return the response body
    response = requests.request(
        "GET", url, auth=(ir1835["username"], ir1835["password"]), headers=headers, verify=False
    )
    response = response.json()

    # Create a field list to help format the routes
    fields = ["destination-prefix", "next-hop-address"]
    data = []

    # Iterate through the returned routes, throughout all the routing instances and append them to a dictionary
    click.secho("Simple JSON format display of the static routes")
    for route in response["ietf-routing:routing"]["routing-instance"][0]["routing-protocols"]["routing-protocol"][0]["static-routes"]["ietf-ipv4-unicast-routing:ipv4"]["route"]:
        line_dict = {}
        line_dict["destination-prefix"] = route["destination-prefix"]
        line_dict["next-hop-address"] = route["next-hop"]["next-hop-address"]
        data.append(line_dict)
        click.echo(json.dumps(route, indent=2))

    # Create a PrettyTable instance and add rows based on the above dictionary
    table = PrettyTable()
    table.field_names = ["Destination", "Next-hop"]
    for row in data:
        table.add_row([row["destination-prefix"], row["next-hop-address"]])
    click.secho("Formatted display of the static routes using PrettyTable")
    click.echo(table)


@click.command(name='get-vlan')
def get_vlan_interfaces():
    """
    Retrieve the VLAN interfaces
    """
    url = f"https://{ir1835['host']}/restconf/data/Cisco-IOS-XE-native:native/interface"

    click.secho("Retrieving VLANs")
    # Make a request and return the response body
    response = requests.request(
        "GET", url, auth=(ir1835["username"], ir1835["password"]), headers=headers, verify=False
    )
    response_json = response.json()

    # Loop through the tenants and print specific details
    click.secho("All the VLAN interfaces with all available details")
    for interface in response_json["Cisco-IOS-XE-native:interface"]["Vlan"]:
        click.echo(json.dumps(interface, indent=3))
        
    click.secho("Only the VLAN IDs")
    for interface in response_json["Cisco-IOS-XE-native:interface"]["Vlan"]:
        click.echo(interface["name"])


@click.command(name='add-vlan')
@click.argument('name')
@click.argument('address')
@click.argument('mask')
def add_vlan_interface(name, address, mask):
    """
    Configure a new VLAN interface on the router
    
    Requires VLAN name, IP, subnet mask

    eg: python ir1835_restconf.py add-vlan 5 5.5.5.5 255.255.255.0
    """
    url = f"https://{ir1835['host']}/restconf/data/Cisco-IOS-XE-native:native/interface"

    click.secho("Creating a new VLAN interface")

    # Create the body payload with the new VLAN interface description
    payload = {
        "Cisco-IOS-XE-native:Vlan": [
            {
                "name": "",
                "description": "RESTCONF test description",
                "ip": {
                    "address": {
                        "primary": {
                            "address": "",
                            "mask": ""
                        }
                    }
                }
            }]
    }

    # Format the payload based on the user CLI inputs
    payload["Cisco-IOS-XE-native:Vlan"][0]["name"] = name
    payload["Cisco-IOS-XE-native:Vlan"][0]["ip"]["address"]["primary"]["address"] = address
    payload["Cisco-IOS-XE-native:Vlan"][0]["ip"]["address"]["primary"]["mask"] = mask
    payload = json.dumps(payload)

    # Make Login request and return the response body
    response = requests.request(
        "POST", url, auth=(ir1835["username"], ir1835["password"]), headers=headers, data=payload, verify=False
    )

    # Retrieve from the APIC's response the login Token
    click.echo(response)


cli.add_command(get_running_config)
cli.add_command(get_static_routes)
cli.add_command(add_vlan_interface)
cli.add_command(get_vlan_interfaces)

# Entry point for program
if __name__ == "__main__":
    cli()
