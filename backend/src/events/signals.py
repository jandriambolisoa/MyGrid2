"""
This file list signals to be used for secondary actions.
"""

from backend.signals import Signal

# championships signals
create_championship = Signal("create_championship")
delete_championship = Signal("delete_championship")

# events signals
create_event = Signal("create_event")
delete_event = Signal("delete_event")

# sessions signals
create_session = Signal("create_session")
delete_session = Signal("delete_session")
