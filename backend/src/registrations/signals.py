"""
This file list signals to be used for secondary actions.
"""

from blinker import Namespace

registrations_namespace = Namespace()

updated_session_registrations = registrations_namespace.signal("updated_sessions_registrations")