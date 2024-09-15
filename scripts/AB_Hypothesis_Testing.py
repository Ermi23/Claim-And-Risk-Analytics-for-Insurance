import pandas as pd
from scipy import stats
from scipy.stats import chi2_contingency, ttest_ind, f_oneway
from statsmodels.stats.proportion import proportions_ztest

class ABHypothesisTesting:
    def __init__(self, data):
        self.data = data

    def check_missing_data(self, df):
        """
        Check for missing data in a DataFrame and return a summary of missing values.
        
        Parameters:
        - df: Pandas DataFrame
        
        Returns:
        - DataFrame: Summary of missing data with counts and percentages
        """
        missing_data = df.isnull().sum()
        missing_data_summary = pd.DataFrame({
            'Column Name': missing_data.index,
            'Missing Values': missing_data.values,
            'Percentage Missing': (missing_data.values / len(df)) * 100
        })
        
        # Ensure all columns are included, even those without missing values
        missing_data_summary['Missing Values'] = missing_data_summary['Missing Values'].fillna(0)
        missing_data_summary['Percentage Missing'] = missing_data_summary['Percentage Missing'].fillna(0)
        
        # Return the summary with all columns
        return missing_data_summary
    
    def run_test(self, df_subset):
        """Run appropriate A/B hypothesis tests based on the column types in the dataframe."""
        # Identify the columns
        cols = df_subset.columns
        
        # Initialize result dictionary
        results = {}

        # Check if we are comparing categorical data (Chi-square or Proportions Z-Test)
        if df_subset[cols[1]].dtype == 'object' or pd.api.types.is_categorical_dtype(df_subset[cols[1]]):
            # Example: testing risk differences (binary outcome like claims/no-claims) across categories (like Province, PostalCode)
            
            if df_subset[cols[0]].dtype == 'int' or df_subset[cols[0]].dtype == 'float':
                # Use a threshold if needed (for binary outcome)
                threshold = 1000
                # df_subset['RiskyClaims'] = df_subset[cols[0]] > threshold
                df_subset.loc[:, 'RiskyClaims'] = df_subset[cols[0]] > threshold

                # Contingency table
                contingency_table = pd.crosstab(df_subset[cols[1]], df_subset['RiskyClaims'])
                
                # Perform chi-square test for independence
                chi2, p, dof, expected = chi2_contingency(contingency_table)
                results['test_type'] = 'Chi-Square Test'
                results['chi2_stat'] = chi2
                results['p_value'] = p
                results['dof'] = dof

            else:
                # For comparing proportions directly between two groups
                unique_groups = df_subset[cols[1]].unique()
                if len(unique_groups) == 2:
                    # Example: Z-test for comparing proportions between two provinces/genders
                    group_a = df_subset[df_subset[cols[1]] == unique_groups[0]]
                    group_b = df_subset[df_subset[cols[1]] == unique_groups[1]]
                    
                    count_a = (group_a[cols[0]] > threshold).sum()
                    count_b = (group_b[cols[0]] > threshold).sum()
                    
                    nobs_a = len(group_a)
                    nobs_b = len(group_b)
                    
                    z_stat, p_value = proportions_ztest([count_a, count_b], [nobs_a, nobs_b])
                    
                    results['test_type'] = 'Proportions Z-Test'
                    results['z_stat'] = z_stat
                    results['p_value'] = p_value

        # For numerical comparisons (T-Test or ANOVA)
        elif df_subset[cols[0]].dtype == 'int' or df_subset[cols[0]].dtype == 'float':
            if df_subset[cols[1]].nunique() == 2:
                # Two-sample T-test (e.g., for comparing TotalPremium between two PostalCodes or Genders)
                group_a = df_subset[df_subset[cols[1]] == df_subset[cols[1]].unique()[0]][cols[0]]
                group_b = df_subset[df_subset[cols[1]] == df_subset[cols[1]].unique()[1]][cols[0]]
                
                t_stat, p_value = ttest_ind(group_a, group_b)
                
                results['test_type'] = 'Two-Sample T-Test'
                results['t_stat'] = t_stat
                results['p_value'] = p_value
            
            else:
                # ANOVA for comparing more than two groups (e.g., TotalPremium across multiple PostalCodes)
                groups = [df_subset[df_subset[cols[1]] == category][cols[0]] for category in df_subset[cols[1]].unique()]
                f_stat, p_value = f_oneway(*groups)
                
                results['test_type'] = 'ANOVA'
                results['f_stat'] = f_stat
                results['p_value'] = p_value

        return results
