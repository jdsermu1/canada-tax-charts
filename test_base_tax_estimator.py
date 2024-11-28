import base_tax_estimator
import unittest
import numpy as np

class TestBaseTaxEstimator(unittest.TestCase):
    
    def test_bucket_odd(self):
        baseEstimator = base_tax_estimator.TaxEstimator(np.array([0, 10, 20]), np.array([.1, .2, .3]))
        self.assertEqual(baseEstimator.bucket(0), 0)
        self.assertEqual(baseEstimator.bucket(5), 0)
        self.assertEqual(baseEstimator.bucket(10), 1)
        self.assertEqual(baseEstimator.bucket(15), 1)
        self.assertEqual(baseEstimator.bucket(20), 2)
        self.assertEqual(baseEstimator.bucket(1000), 2)

    def test_bucket_even(self):
        baseEstimator = base_tax_estimator.TaxEstimator(np.array([0, 10, 20, 30]), np.array([.1, .2, .3, .4]))
        self.assertEqual(baseEstimator.bucket(0), 0)
        self.assertEqual(baseEstimator.bucket(5), 0)
        self.assertEqual(baseEstimator.bucket(10), 1)
        self.assertEqual(baseEstimator.bucket(15), 1)
        self.assertEqual(baseEstimator.bucket(20), 2)
        self.assertEqual(baseEstimator.bucket(25), 2)
        self.assertEqual(baseEstimator.bucket(30), 3)
        self.assertEqual(baseEstimator.bucket(1000), 3)

    def test_tax(self):
        baseEstimator = base_tax_estimator.TaxEstimator(np.array([0, 10, 20, 30]), np.array([.1, .2, .3, .4]))
        self.assertEqual(baseEstimator.tax(0), 0)
        self.assertEqual(baseEstimator.tax(5), .5)
        self.assertEqual(baseEstimator.tax(10), 1)
        self.assertEqual(baseEstimator.tax(15), 2)
        self.assertEqual(baseEstimator.tax(20), 3)
        self.assertEqual(baseEstimator.tax(25), 4.5)
        self.assertEqual(baseEstimator.tax(30), 6)
        self.assertEqual(baseEstimator.tax(35), 8)
    


if __name__ == '__main__':
    unittest.main()
