"""
This file list signals to be used for secondary actions.
"""

from blinker import Namespace

users_namespace = Namespace()

# CRUD signals
created = users_namespace.signal("created")
read = users_namespace.signal("read")
updated = users_namespace.signal("updated")
deleted = users_namespace.signal("deleted")

# Connexions signals
connects = users_namespace.signal("connects")
disconnects = users_namespace.signal("disconnects")