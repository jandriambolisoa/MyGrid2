"""
This file list signals to be used for secondary actions.
"""

from backend.signals import Signal

# championships signals
create_league = Signal("create_league")
update_league = Signal("update_league")
delete_league = Signal("delete_league")