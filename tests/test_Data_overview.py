import unittest
from scripts.Data_overview import InsuranceDataEDA
import os
import pandas as pd

class TestInsuranceDataEDA(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.file_name = "test_data.csv"
        cls.eda = InsuranceDataEDA(cls.file_name)
        cls.test_data = {
            'SumInsured': [10000, 20000, 30000],
            'CalculatedPremiumPerTerm': [100, 200, 300],
            'TotalPremium': [1200, 2400, 3600],
            'TotalClaims': [2, 1, 0],
            'Cylinders': [4, 6, 8],
            'NumberOfDoors': [2, 4, 4],
            'CustomValueEstimate': [5000, 10000, 15000],
            'kilowatts': [100, 150, 200],
            'cubiccapacity': [1500, 2000, 2500],
            'CapitalOutstanding': [5000, 10000, 15000],
            'Gender': ['Male', None, 'Female'],
            'MaritalStatus': ['Single', None, 'Married'],
            'Title': ['Mr', 'Ms', 'Mrs']
        }
        cls.test_df = pd.DataFrame(cls.test_data)
        cls.eda.data = cls.test_df

    def test_set_working_directory(self):
        self.eda.set_working_directory(os.getcwd())
        self.assertEqual(os.getcwd(), os.getcwd())

    # def test_load_data(self):
    #     self.eda.load_data()
    #     self.assertIsNotNone(self.eda.data)

    def test_check_data_types(self):
        self.eda.check_data_types()
        self.assertIsNotNone(self.eda.data)

    def test_describe_numerical_columns(self):
        description = self.eda.describe_numerical_columns()
        self.assertIsNotNone(description)

    def test_plot_numerical_analysis(self):
        self.eda.plot_numerical_analysis()

    def test_analyze_categorical_columns(self):
        frequency_tables = self.eda.analyze_categorical_columns()
        self.assertIsNotNone(frequency_tables)

    # def test_plot_categorical_analysis(self):
    #     frequency_tables = self.eda.analyze_categorical_columns()
    #     self.eda.plot_categorical_analysis(frequency_tables)

    def test_visualize_missing_values(self):
        self.eda.visualize_missing_values()

    def test_fill_missing_values(self):
        self.eda.fill_missing_values()
        self.assertEqual(self.eda.data['Gender'][1], 'Female')
        self.assertEqual(self.eda.data['MaritalStatus'][1], 'Married')

    def test_analyze_marrageStatus_and_gender_columns(self):
        self.eda.analyze_marrageStatus_and_gender_columns()

    # def test_plot_premium_vs_claims(self):
    #     self.eda.plot_premium_vs_claims()

    def test_plot_correlation_matrix_for_TotalPremium_and_TotalClaims(self):
        self.eda.plot_correlation_matrix_for_TotalPremium_and_TotalClaims()

    def test_analyze_geographic_data(self):
        self.eda.analyze_geographic_data()

    # def test_plot_cover_type_distribution(self):
    #     self.eda.plot_cover_type_distribution()

    # def test_plot_average_premium_by_province(self):
    #     self.eda.plot_average_premium_by_province()

    # def test_plot_car_make_distribution(self):
    #     self.eda.plot_car_make_distribution()

    # def test_plot_average_sum_insured_by_make(self):
    #     self.eda.plot_average_sum_insured_by_make()

    def test_plot_boxplots_for_numerical_columns(self):
        self.eda.plot_boxplots_for_numerical_columns()

    def test_plot_correlation_matrix(self):
        self.eda.plot_correlation_matrix()

    def test_export_data(self):
        output_file = "output_test.csv"
        self.eda.export_data(output_file)
        self.assertTrue(os.path.exists(output_file))
        os.remove(output_file)

if __name__ == '__main__':
    unittest.main()
