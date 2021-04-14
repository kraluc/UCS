#!/usr/bin/env python

# Examples from Cisco Live Preso
# https://www.ciscolive.com/c/dam/r/ciscolive/us/docs/2020/pdf/DGTL-BRKPRG-2432.pdf

''' Example 3 '''

# Create a Login HANDLE and Login
from ucsmsdk.ucshandle import UcsHandle
HANDLE = UcsHandle("172.16.125.2", "ucspe", "ucspe" )

# Query Filters and descriptions
Q_FILTERS = [
    {
        'filter_exp': '(model, "UCSB-[1-zA-Z0-9]*-M4[\-a-zA-Z0-9]*", type="re")',
        'filter_des': '"model matches UCSB-[a-zA-Z0-9]*"'
    },
    {
        'filter_exp': '(model, "UCSB-B200-M4", type="eq")',
        'filter_des': '"model equals UCSB-B200-M4"'
    },
    {
        'filter_exp': '(model, "UCSB-B200-M4", type="ne")',
        'filter_des': '"model not equal UCSB-B200-M4"'
    },
    {
        'filter_exp': '(model,"ucsB-B200-m4", flag="I")',
        'filter_des': '"model matches ucsB-B200-m4 case insensitive"'
    }
]

# Login
HANDLE.login()

# Print HANDLE 'cookie' attribute
print(f"cookie: {HANDLE.cookie}")

# Iterate over the Q_FILTERS dictionary and display the results
for q_filter in Q_FILTERS:
    blades = HANDLE.query_classid(
        "ComputeBlade", filter_str=q_filter['filter_exp']
    )
    print(f"\nUCS Query for {q_filter['filter_des']}")
    print(f" Number of blades found: {len(blades)}")

# Logout
HANDLE.logout()