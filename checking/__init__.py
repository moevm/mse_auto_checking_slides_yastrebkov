from .checker import Checker

from .checks.relevance_presence import RelevancePresence
Checker.add(RelevancePresence, 0)

from .checks.approbation_presence import ApprobationPresence
Checker.add(ApprobationPresence, 1)

from .checks.conclusion_presence import ConclusionPresence
Checker.add(ConclusionPresence, 2)

from .checks.slides_amount import SlidesAmount
Checker.add(SlidesAmount, 3)

from .checks.slide_numbers import SlideNumbers
Checker.add(SlideNumbers, 4)
