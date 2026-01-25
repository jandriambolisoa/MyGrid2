"""
This file list signals to be used for secondary actions.
"""

from backend.signals import Signal

# CRUD signals
created = Signal("created")
read = Signal("read")
updated = Signal("updated")
deleted = Signal("deleted")

# Connexions signals
connects = Signal("connects")
disconnects = Signal("disconnects")
