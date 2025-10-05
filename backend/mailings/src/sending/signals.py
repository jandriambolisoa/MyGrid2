"""
This file list signals to be used for secondary actions.
"""

from blinker import Namespace

mailings_namespace = Namespace()

# Connexions signals
sent = mailings_namespace.signal("sent")