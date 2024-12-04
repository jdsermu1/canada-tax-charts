import base_tax_estimator
import exceptions


class DividendTaxCreditor:
    def __init__(self, elegible_tax_credit_rate, non_elegible_tax_credit):
        self.__eligible_tax_credit_rate = elegible_tax_credit_rate
        self.___non_elegible_tax_creidt_rate = non_elegible_tax_credit

    def validate(self):
        if not 0 <= self.__tax_credit_rate <= 1:
            raise exceptions.EstimatorError("Tax credit rate should be between 0 and 1")

    def tax_credit(self, value, elegible=False):
        return (
            self.__eligible_tax_credit_rate if elegible else self.___non_elegible_tax_creidt_rate
        ) * value


class ProvinceTaxEstimator:
    def __init__(self, province: str, limits, rates):
        self.__province = province
        self.__base = base_tax_estimator.TaxEstimator(limits, rates)

    def province(self) -> str:
        return self.__province

    def tax(self, value):
        return self.__base.tax(value)


class CanadaTaxEstimator:
    def __init__(self, federal_limits, federal_rates):
        self.__province_repositoy: dict[str, ProvinceTaxEstimator] = {}
        self.__federal_estimator: ProvinceTaxEstimator = ProvinceTaxEstimator(
            "Federal", federal_limits, federal_rates
        )

    def addProvince(self, province: str, limits, rates):
        self.__province_repositoy[province] = ProvinceTaxEstimator(
            province, limits, rates
        )

    def getProvince(self, province):
        province_estimator = self.__province_repositoy.get(province)
        if province_estimator is None:
            raise exceptions.EstimatorError(
                "There's no provincial estimator for " + province
            )
        return province_estimator

    def getProvinces(self) -> list[str]:
        return list(self.__province_repositoy.keys())

    def tax(self, province, value, cg_pc=0.0):
        if not 0.0 <= cg_pc <= 1.0:
            raise exceptions.EstimatorError(
                "Capital gain percentage should be between 0 and 1"
            )
        province_estimator: ProvinceTaxEstimator = self.__province_repositoy.get(
            province
        )
        if province_estimator is None:
            raise exceptions.EstimatorError(
                "There's no provincial estimator for " + province
            )

        cg_threshold = 250000

        adj_value = (
            (1 - cg_pc) * value
            + min(cg_pc * value, cg_threshold) / 2
            + max(cg_pc * value - cg_threshold, 0) * 2 / 3
        )

        return self.__federal_estimator.tax(adj_value) + province_estimator.tax(
            adj_value
        )

    def average_tax_rate(self, province, value, cg_pc=0.0):
        if value == 0:
            return 0
        return self.tax(province, value, cg_pc=cg_pc) / value
