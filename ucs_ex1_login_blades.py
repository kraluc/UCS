#!/usr/bin/env python

# Examples from Cisco Live Preso
# https://www.ciscolive.com/c/dam/r/ciscolive/us/docs/2020/pdf/DGTL-BRKPRG-2432.pdf

''' Example 1 '''

# Create a Login HANDLE and Login
from ucsmsdk.ucshandle import UcsHandle
HANDLE = UcsHandle("172.16.125.2", "ucspe", "ucspe" )
HANDLE.login()

# Print HANDLE 'cookie' attribute
print(f"\ncookie: {HANDLE.cookie}")

# Query Compute blades and print number of object returned
# Queries are executed with a HANDLE member method
BLADES = HANDLE.query_classid('ComputeBlade')
print(f"\nNumber of blades found: {len(BLADES)}\n")

# Iterate of blade list displaying attributes from each object
for blade in BLADES:
    print(blade.dn, blade.serial, blade.model)

# Turn on UCS XML API view to dump XML that is sent and received
# HANDLE.set_dump_xml()
# BLADES = HANDLE.query_classid("ComputeBlade")
# HANDLE.unset_dump_xml()

# Logout
HANDLE.logout()