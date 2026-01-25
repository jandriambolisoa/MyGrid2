"""
This file list signals to be used for secondary actions.
"""

from backend.signals import Signal

# drivers signals
create_driver = Signal("create_driver")
delete_driver = Signal("delete_driver")

# teams signals
create_team = Signal("create_team")
delete_team = Signal("delete_team")