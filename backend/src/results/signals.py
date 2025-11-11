"""
This file list signals to be used for secondary actions.
"""

from blinker import Namespace

from backend.src.scores.listener import compute_session_score

results_namespace = Namespace()

updated_session_results = results_namespace.signal("updated_session_results")
delete_session_results = results_namespace.signal("delete_session_results")
