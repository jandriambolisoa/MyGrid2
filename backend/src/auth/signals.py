"""
This file list signals to be used for secondary actions.
"""

from blinker import Namespace

auth_namespace = Namespace()

# Auth signals
validate_mail = auth_namespace.signal("validate_mail")