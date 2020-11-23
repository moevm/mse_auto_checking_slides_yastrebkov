from .checker import Checker

from .checks.relevance_presence import RelevancePresence
Checker.add(RelevancePresence, 0)

from .checks.approbation_presence import ApprobationPresence
Checker.add(ApprobationPresence, 1)
