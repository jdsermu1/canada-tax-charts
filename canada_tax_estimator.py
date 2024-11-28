import base_tax_estimator
import exceptions


class ProvinceTaxEstimator:
    def __init__(self, province: str, limits, rates):
        self.__province = province
        self.__base = base_tax_estimator.TaxEstimator(limits, rates)

    def province(self)->str:
        return self.__province
    
    def tax(self, value):
        return self.__base.tax(value)


class CanadaTaxEstimator:
    def __init__(self, federal_limits, federal_rates):
        self.__province_repositoy:dict[str, ProvinceTaxEstimator] = {}
        self.__federal_estimator:ProvinceTaxEstimator = ProvinceTaxEstimator("Federal", federal_limits, federal_rates)

    def addProvince(self, province:str, limits, rates):
        self.__province_repositoy[province] = ProvinceTaxEstimator(province, limits, rates)

    def getProvince(self, province):
        province_estimator = self.__province_repositoy.get(province)
        if province_estimator is None:
            raise exceptions.EstimatorError("There's no provincial estimator for " + province)
        return province_estimator
    
    def getProvinces(self) -> list[str]:
        return list(self.__province_repositoy.keys())

    def tax(self, province, value):
        province_estimator:ProvinceTaxEstimator = self.__province_repositoy.get(province)
        if province_estimator is None:
            raise exceptions.EstimatorError("There's no provincial estimator for " + province)
        return self.__federal_estimator.tax(value) + province_estimator.tax(value)
    
    def tax_rate(self, province, value):
        if value == 0:
            return 0
        return self.tax(province, value)/value
    
    def tax_func(self, province):
        return lambda value: self.tax(province, value)
    
    def tax_rate_func(self, province):
        return lambda value: self.tax_rate(province, value)