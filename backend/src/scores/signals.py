"""
This file list signals to be used for secondary actions.
"""

from blinker import Namespace

scores_namespace = Namespace()

updated_championship_scores = scores_namespace.signal("updated_championship_scores")
