"""
This file list signals to be used for secondary actions.
"""

from backend.signals import Signal

# Auth signals
request_reset_password = Signal("request_reset_password")
validate_mail = Signal("validate_mail")