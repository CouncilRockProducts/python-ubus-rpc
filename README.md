OpenWrt ubus RPC Python API
===========================

[![License: GPL v2][gpl2-button]](LICENSE.md)

[gpl2-button]: https://img.shields.io/badge/License-GPL%20v2-blue.svg

Python client for the OpenWrt ubus RPC API.

This fork contains a modified version of [Noltari](https://github.com/Noltari)'s code as used by the [Council Rock products group](https://github.com/orgs/CouncilRockProducts).

Description
-----------

openwrt-ubus-rpc is a Python module implementing an interface to the OpenWrt ubus RPC API.  
It allows a user to perform Remote Procedure Calls (RPC) to the OpenWrt micro bus architecture (ubus).

Documentation for the OpenWrt ubus RPC API is available at https://openwrt.org/docs/techref/ubus and https://openwrt.org/docs/guide-developer/ubus.

This package has been developed to be used with https://home-assistant.io/ but it can be used in other contexts.

Disclaimer
----------

openwrt-ubus-rpc was created for [Noltari](https://github.com/Noltari)'s own use, and for others who may wish to experiment with personal Internet of Things systems.

This software is provided without warranty, according to the GNU Public Licence version 2, and should therefore not be used where it may endanger life, financial stakes or cause discomfort and inconvenience to others.

Usage
-----

```python
from openwrt.ubus import Ubus
_ubus = Ubus.connect(f"https://{host}/ubus", "root", password)
_ubus.call_rpc("system", "board")
```
