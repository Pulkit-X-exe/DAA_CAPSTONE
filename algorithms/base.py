"""
Abstract Base Class and Type Definitions for DAA String Matching Algorithms.
Defines unified structure, dataclasses, and contracts for all string search algorithms.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List


@dataclass
class MatchResult:
    """
    Standardized return structure for algorithm executions.
    """
    algorithm_name: str
    matches: List[int] = field(default_factory=list)
    comparisons: int = 0
    collisions: int = 0  # Relevant for Rabin-Karp
    execution_time_ms: float = 0.0


class StringMatchingAlgorithm(ABC):
    """
    Abstract interface that all DAA pattern matching algorithms implement.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Returns the human-readable algorithm name."""
        pass

    @property
    @abstractmethod
    def worst_case_complexity(self) -> str:
        """Returns the asymptotic worst-case time complexity."""
        pass

    @property
    @abstractmethod
    def space_complexity(self) -> str:
        """Returns the auxiliary space complexity."""
        pass

    @abstractmethod
    def search(self, text: str, pattern: str) -> MatchResult:
        """
        Executes the string matching algorithm.

        Args:
            text (str): The haystack text.
            pattern (str): The needle pattern.

        Returns:
            MatchResult: Dataclass containing match indices and operation stats.
        """
        pass
