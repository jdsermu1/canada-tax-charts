import abc
import exceptions


class TaxEstimatorInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, "tax") and callable(subclass.tax)


class TaxEstimator:
    def __init__(self, limits, rates):
        if len(limits) == 0 or len(rates) == 0:
            raise exceptions.EstimatorError("limits/rates not provided")
        if len(limits) != len(rates):
            raise exceptions.EstimatorError(
                "limits and rates should have the same size"
            )
        if limits[0] != 0:
            raise exceptions.EstimatorError(
                "First lower limit should be 0 currently is " + limits[0]
            )
        if not all(limits[i] <= limits[i + 1] for i in range(len(limits) - 1)):
            raise exceptions.EstimatorError("Limits should be in ascending order")
        self.__limits = limits
        self.__rates = rates
        self.__functions = TaxEstimator.tax_functions(self.__limits, self.__rates)

    @staticmethod
    def tax_functions(limits, rates):
        functions = [(0, 0)] * len(limits)
        for i, lower_limit in enumerate(limits):
            c = (
                0
                if i == 0
                else functions[i - 1][1]
                + functions[i - 1][0] * (lower_limit - limits[i - 1])
            )
            functions[i] = (rates[i], c)
        return functions

    def __bucket(self, low, high, value):
        if low > high:
            raise exceptions.EstimatorError(
                "Was not possible to find the bucket for value " + str(value)
            )
        if value >= self.__limits[high]:
            return high
        mid = int((low + high) / 2)
        if self.__limits[mid] == value:
            return mid
        if mid > 0 and self.__limits[mid - 1] <= value and value < self.__limits[mid]:
            return mid - 1
        if value < self.__limits[mid]:
            return self.__bucket(low, mid - 1, value)
        return self.__bucket(mid + 1, high, value)

    def bucket(self, value: float):
        return self.__bucket(0, len(self.__limits) - 1, value)

    def tax(self, value):
        if value < 0:
            raise exceptions.EstimatorError(
                "Ca't calculate tax for negative value: " + str(value)
            )
        bucket = self.bucket(value)
        return float(
            self.__functions[bucket][0] * (value - self.__limits[bucket])
            + self.__functions[bucket][1]
        )

    def average_tax_rate(self, value):
        if value == 0:
            return 0
        return self.tax(value) / value
