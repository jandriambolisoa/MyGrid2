"""
This file list signals to be used for secondary actions.
"""

from backend.signals import Signal

updated_session_results = Signal("updated_session_results")
delete_session_results = Signal("delete_session_results")
