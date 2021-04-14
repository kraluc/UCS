#!/usr/bin/env python

# Examples from Cisco Live Preso
# https://www.ciscolive.com/c/dam/r/ciscolive/us/docs/2020/pdf/DGTL-BRKPRG-2432.pdf

''' Example 4 '''

# Create a Login HANDLE and Login
from ucsmsdk.ucshandle import UcsHandle
HANDLE = UcsHandle("172.16.125.2", "ucspe", "ucspe" )

# Login
HANDLE.login()

# Print HANDLE 'cookie' attribute
print("cookie:" + HANDLE.cookie)

# List of Objects Returned
BLADES = HANDLE.query_classid("ComputeBlade")
print(BLADES)

# Single Object Returned
BLADE_BY_DN = HANDLE.query_dn("sys/chassis-3/blade-1")
print(BLADE_BY_DN)

# Dictionary of Object Lists Returned Key is the ClassId
BLADES_AND_CHASSIS = HANDLE.query_classids(
    "ComputeBlade",
    "EquipmentChassis"
)
print(BLADES_AND_CHASSIS)

# Access each returned Class Objects by the ClassId
print(BLADES_AND_CHASSIS['EquipmentChassis'])
for chassis in BLADES_AND_CHASSIS['EquipmentChassis']:
    print(chassis.dn, chassis.model)

print(BLADES_AND_CHASSIS['ComputeBlade'])
for blade in BLADES_AND_CHASSIS['ComputeBlade']:
    print(blade.dn, blade.model)

# Dictionary of dn as the key and objects as the value
BLADES_AND_CHASSIS = HANDLE.query_dns(
    "sys/chassis-3/blade-1",
    "sys/chassis-4"
)

# Logout
HANDLE.logout()