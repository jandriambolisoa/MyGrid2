"""
This file list signals to be used for secondary actions.
"""

from blinker import Namespace

events_namespace = Namespace()

# championships signals
create_championship = events_namespace.signal("create_championship")
delete_championship = events_namespace.signal("delete_championship")

# events signals
create_event = events_namespace.signal("create_event")
delete_event = events_namespace.signal("delete_event")

# sessions signals
create_session = events_namespace.signal("create_session")
delete_session = events_namespace.signal("delete_session")
