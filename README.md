<h2 align="center">IOS XE Device Programmability</h2>
<div align="center">
</div>

---

## Table of Contents

- [About](#about)
- [How to Run](#run)

##  About <a name = "about"></a>

A small collection of simple Python scripts & Ansible playbooks to perform various tasks on IOS XE devices 

 using either RESTCONF/NETCONF or CLI through the "network_cli" Ansible module.

<br>

## Prerequisites<a name = "prequisites"></a>

Tested using the below tools:

- Python - 3.8.5+
- Ansible - 2.12.4+

<br>

## How to run <a name = "run"></a>


### Setting up environment:

```bash
$ git clone <repo>
$ pip install -r requirements.txt
```

### Working with the scripts 
```bash
# RESTCONF
python ir1835_restconf.py --help #displays the possible commands
python ir1835_restconf.py <command> --help    #displays additional help related to that specific command

eg. python ir1835_restconf.py add-vlan 5 5.5.5.5 255.255.255.0

# NETCONF
python ir1835_netconf.py --help #displays the possible commands
python ir1835_netconf.py <command> --help #displays additional help related to that specific command

eg. python ir1835_netconf.py get-request retrieve_vlan_interfaces.xml

# Ansible
cd ansible-playbooks #easier to work from this dir
ansible-playbook --inventory=hosts  ansible-<ios-modules/netconf-config>/<playbook.yaml>                             

eg. ansible-playbook --inventory=hosts  ansible-ios-modules/ios_command_show.yaml   
```