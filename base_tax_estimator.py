import abc
from typing import List, Tuple, Union
from functools import lru_cache


class TaxEstimatorInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, "tax") and callable(subclass.tax)


class TaxEstimator:
    def __init__(self, limits: List[float], rates: List[float]) -> None:
        # Cache length and validate inputs
        self.__length: int = len(limits)
        self.__validate_inputs(limits, rates)

        # Store as tuple for immutability
        self.__limits: Tuple[float, ...] = tuple(limits)
        self.__rates: Tuple[float, ...] = tuple(rates)
        self.__functions: List[Tuple[float, float]] = self.__calculate_tax_functions()

    def __validate_inputs(self, limits: List[float], rates: List[float]) -> None:
        """Validate input parameters."""
        if not self.__length or rates is None:
            raise ValueError("limits/rates not provided")
        if self.__length != len(rates):
            raise ValueError("limits and rates should have the same size")
        if limits[0] != 0:
            raise ValueError(f"First lower limit should be 0, currently is {limits[0]}")
        if any(limits[i] > limits[i + 1] for i in range(self.__length - 1)):
            raise ValueError("Limits should be in ascending order")

    def __calculate_tax_functions(self) -> List[Tuple[float, float]]:
        """Calculate tax functions with optimized loop."""
        functions = [(self.__rates[0], 0.0)]
        prev_rate, prev_sum = self.__rates[0], 0.0

        for i in range(1, self.__length):
            bracket_size = self.__limits[i] - self.__limits[i - 1]
            current_sum = prev_sum + prev_rate * bracket_size
            functions.append((self.__rates[i], current_sum))
            prev_rate, prev_sum = self.__rates[i], current_sum

        return functions

    @lru_cache(maxsize=128)
    def bucket(self, value: float) -> int:
        """
        Find the appropriate tax bracket using optimized binary search.
        Cache results for frequently accessed values.
        """
        left, right = 0, self.__length - 1

        while left <= right:
            mid = (left + right) >> 1

            # Check if value is in current bracket
            if mid > 0 and self.__limits[mid - 1] <= value < self.__limits[mid]:
                return mid - 1

            # Check if value is in highest bracket
            if value >= self.__limits[right]:
                return right

            if value < self.__limits[mid]:
                right = mid - 1
            else:
                left = mid + 1

        raise ValueError(f"Could not find bucket for value {value}")

    def tax(self, value: float) -> float:
        """Calculate tax with optimized computation."""
        if value < 0:
            raise ValueError(f"Can't calculate tax for negative value: {value}")

        bucket_index = self.bucket(value)
        rate, base_tax = self.__functions[bucket_index]

        return rate * (value - self.__limits[bucket_index]) + base_tax

    def average_tax_rate(self, value: float) -> float:
        """Calculate average tax rate with null check optimization."""
        return 0.0 if value <= 0 else self.tax(value) / value
