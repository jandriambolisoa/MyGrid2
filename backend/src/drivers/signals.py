"""
This file list signals to be used for secondary actions.
"""

from blinker import Namespace

drivers_namespace = Namespace()

# drivers signals
create_driver = drivers_namespace.signal("create_driver")
delete_driver = drivers_namespace.signal("delete_driver")

# teams signals
create_team = drivers_namespace.signal("create_team")
delete_team = drivers_namespace.signal("delete_team")