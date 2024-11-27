import numpy as np
import abc

class EstimatorError(Exception):
    def __init__(self, message:str, *args):
        self.message = message
        super().__init__(*args)

class TaxEstimatorInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, 'tax') and callable(subclass.tax)

class BaseTaxEstimator:
    def __init__(self, limits, rates):
        if len(limits) == 0 or len(rates) == 0:
            raise EstimatorError("limits/rates not provided")
        if len(limits) != len(rates):
            raise EstimatorError("limits and rates should have the same size")
        if limits[0] != 0:
            raise EstimatorError("First lower limit should be 0 currently is " + limits[0])
        if not all(limits[i]<=limits[i+1] for i in range(len(limits)-1)):
            raise EstimatorError("Limits should be in ascending order")
        self.__limits = limits
        self.__rates = rates
        self.__functions = BaseTaxEstimator.tax_functions(self.__limits, self.__rates)

    @staticmethod
    def tax_functions(limits, rates):
        functions = [(0,0)]*len(limits)
        for  i, lower_limit in enumerate(limits):
            c = 0 if i==0 else functions[i-1][1]+functions[i-1][0]*(lower_limit-limits[i-1])
            functions[i] = (rates[i], c)
        return functions
    
    def bucket(self, value: float):
        if value<0:
            raise EstimatorError("can't find bucket for negative value "+value)
        low, high = 0, len(self.__limits)-1
        while low <= high:
            mid = low + (high-low)//2
            if mid == len(self.__limits)-1:
                return len(self.__limits)-1
            if self.__limits[mid]<=value<self.__limits[mid+1]:
                return mid
            elif self.__limits[mid]>value:
                high = mid-1
            else:
                low = mid+1
        raise EstimatorError("Was not possible to find the bucket for value " + value)


    def tax(self, value):
        bucket = self.bucket(value)
        return float(self.__functions[bucket][0]*(value-self.__limits[bucket]) + self.__functions[bucket][1])


class ProvinceTaxEstimator:
    def __init__(self, province: str, limits, rates):
        self.__province = province
        self.__base = BaseTaxEstimator(limits, rates)

    def province(self)->str:
        return self.__province


class CanadaTaxEstimator:
    def __init__(self):
        self.__province_repositoy = {}
    