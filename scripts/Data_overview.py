import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class InsuranceDataEDA:
    def __init__(self, file_name):
        self.file_name = file_name
        self.data = None
        self.columns = {
            "insurance_policy": ["UnderwrittenCoverID", "PolicyID", "TransactionMonth"],
            "client_info": ["IsVATRegistered", "Citizenship", "LegalType", "Title", "Language", "Bank", "AccountType", "MaritalStatus", "Gender"],
            "client_location": ["Country", "Province", "PostalCode", "MainCrestaZone", "SubCrestaZone"],
            "car_insured": ["ItemType", "mmcode", "VehicleType", "RegistrationYear", "make", "Model", "Cylinders", "cubiccapacity", "kilowatts", "bodytype", "NumberOfDoors", "VehicleIntroDate", "CustomValueEstimate", "AlarmImmobiliser", "TrackingDevice"],
            "plan": ["SumInsured", "TermFrequency", "CalculatedPremiumPerTerm", "ExcessSelected", "CoverCategory", "CoverType", "CoverGroup", "Section", "Product", "StatutoryClass", "StatutoryRiskType"],
            "payment_claim": ["TotalPremium", "TotalClaims", "CapitalOutstanding", "NewVehicle", "WrittenOff", "Rebuilt", "Converted", "CrossBorder", "NumberOfVehiclesInFleet"]
        }
        # self.relevant_numerical_columns = [
        #     'SumInsured', 'CalculatedPremiumPerTerm', 'TotalPremium', 'TotalClaims',
        #     'Cylinders', 'NumberOfDoors', 'CustomValueEstimate', 'kilowatts',
        #     'cubiccapacity', 'CapitalOutstanding'
        # ]
        self.relevant_numerical_columns = [ 
            "cubiccapacity", "kilowatts", "SumInsured", "CalculatedPremiumPerTerm",
            "TotalPremium", "TotalClaims", "CapitalOutstanding"
            ]
        # self.relevant_categorical_columns = [
        #     "IsVATRegistered", 'TermFrequency', "LegalType", "Bank", "AccountType",
        #     "MaritalStatus", "Gender", "Country", "ItemType", "VehicleType",
        #     "RegistrationYear", "AlarmImmobiliser", "TrackingDevice", 'ExcessSelected',
        #     "Section", "Product", "StatutoryClass", "StatutoryRiskType", "CrossBorder",
        #     "CoverCategory", "CoverType", "CoverGroup"
        # ]
        self.relevant_categorical_columns = [
            "IsVATRegistered","Citizenship","LegalType","Title","Language","Bank","AccountType","MaritalStatus", "ExcessSelected",
            "Gender","Country","Province","PostalCode","MainCrestaZone","SubCrestaZone","ItemType","mmcode","VehicleType","RegistrationYear",
            "make","Cylinders","bodytype","NumberOfDoors","CustomValueEstimate","AlarmImmobiliser", "TermFrequency",
            "TrackingDevice","CoverCategory","CoverType","CoverGroup","Section","Product","StatutoryClass","StatutoryRiskType","NewVehicle",
            "WrittenOff","Rebuilt","Converted",  "CrossBorder"
            ]
        # "VehicleIntroDate", "Model", "NumberOfVehiclesInFleet"

    def set_working_directory(self, path):
        os.chdir(path)
        print(f"Working directory set to: {os.getcwd()}")

    def load_data(self):
        file_path = os.path.join('data', self.file_name)
        print(f"Analyzing {self.file_name}")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        else:
            print(f"File found: {file_path}")

        self.data = pd.read_csv(file_path, delimiter='|')
        print(self.data.head())

    def check_data_types(self):
        print(self.data.info())

    def describe_numerical_columns(self):
        # Convert CapitalOutstanding to numeric
        self.data['CapitalOutstanding'] = pd.to_numeric(self.data['CapitalOutstanding'], errors='coerce')
        return self.data[self.relevant_numerical_columns].describe()

    def plot_numerical_analysis(self):
        n_cols = 3
        n_rows = (len(self.relevant_numerical_columns) + n_cols - 1) // n_cols

        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5 * n_rows))
        fig.suptitle('Numerical Column Univariate Analysis', fontsize=16)
        fig.subplots_adjust(top=0.9, bottom=0.1, hspace=0.7, wspace=0.3)

        axes = axes.flatten()

        for idx, column in enumerate(self.relevant_numerical_columns):
            axes[idx].hist(self.data[column], bins=30)
            axes[idx].set_title(f'Distribution of {column}')
            axes[idx].set_xlabel(column)
            axes[idx].set_ylabel('Frequency')
            axes[idx].tick_params(axis='x', rotation=45)

        for i in range(len(self.relevant_numerical_columns), len(axes)):
            fig.delaxes(axes[i])

        plt.show()

    def analyze_categorical_columns(self):
        frequency_tables = []
        for column in self.relevant_categorical_columns:
            value_counts = self.data[column].value_counts().reset_index()
            value_counts.columns = [column, 'Frequency']
            frequency_tables.append(value_counts)

        # Print each frequency table
        for idx, table in enumerate(frequency_tables):
            print(f"Frequency table for {self.relevant_categorical_columns[idx]}:")
            print(table)
            print("\n" + "="*50 + "\n")

        return frequency_tables

    def plot_categorical_analysis(self, frequency_tables):
        n_cols = 3
        n_rows = (len(self.relevant_categorical_columns) + n_cols - 1) // n_cols

        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5 * n_rows))
        fig.suptitle('Categorical Column Univariate Analysis', fontsize=16)
        fig.subplots_adjust(top=0.9, bottom=0.1, hspace=0.7, wspace=0.3)

        axes = axes.flatten()

        for idx, column in enumerate(self.relevant_categorical_columns):
            table = frequency_tables[idx]
            axes[idx].bar(table[column], table['Frequency'], color='skyblue')
            axes[idx].set_title(f'Distribution of {column}')
            axes[idx].set_xlabel(column)
            axes[idx].set_ylabel('Frequency')
            axes[idx].tick_params(axis='x', rotation=90)

        for i in range(len(self.relevant_categorical_columns), len(axes)):
            fig.delaxes(axes[i])

        plt.show()

    def visualize_missing_values(self):
        self.data = self.data.applymap(lambda x: np.nan if isinstance(x, str) and (x.strip() == '' or x == 'Not specified') else x)
        missing_values = self.data.isnull().sum()
        missing_percentage = self.data.isnull().mean() * 100
        data_types = self.data.dtypes

        missing_data_table = pd.DataFrame({
            'Column': missing_values.index,
            'Missing Values': missing_values.values,
            'Percentage': missing_percentage.values,
            'Data Type': data_types.values
        })

        print(missing_data_table)

        plt.figure(figsize=(12, 6))
        sns.heatmap(self.data.isnull(), cbar=False, cmap='viridis')
        plt.title('Missing Values Heatmap')
        plt.xlabel('Columns')
        plt.ylabel('Rows')
        plt.show()

    def fill_missing_values(self):
        gender_filled_count = 0
        marital_status_filled_count = 0

        for index, row in self.data.iterrows():
            if pd.isnull(row['Gender']):
                if row['Title'] in ['Mr', 'Dr']:
                    self.data.at[index, 'Gender'] = 'Male'
                    gender_filled_count += 1
                elif row['Title'] in ['Miss', 'Ms']:
                    self.data.at[index, 'Gender'] = 'Female'
                    gender_filled_count += 1

            if pd.isnull(row['MaritalStatus']):
                if row['Title'] in ['Mr']:
                    self.data.at[index, 'MaritalStatus'] = 'Single'
                    marital_status_filled_count += 1
                elif row['Title'] in ['Mrs', 'Ms']:
                    self.data.at[index, 'MaritalStatus'] = 'Married'
                    marital_status_filled_count += 1

        # Print a summary message
        print(f"Filled {gender_filled_count} 'Gender' values and {marital_status_filled_count} 'MaritalStatus' values using the 'Title' column.")

    def analyze_marrageStatus_and_gender_columns(self):
        gender_and_marrage_status = ["MaritalStatus", "Gender"]

        # Check for missing values only in the relevant columns
        missing_values = self.data[gender_and_marrage_status].isnull().sum()

        # Calculate percentage of missing values
        missing_percentage = self.data[gender_and_marrage_status].isnull().mean() * 100

        # Get data types of each relevant column
        data_types = self.data[gender_and_marrage_status].dtypes

        # Create a DataFrame to display the results
        missing_data_table = pd.DataFrame({
            'Column': missing_values.index,
            'Missing Values': missing_values.values,
            'Percentage': missing_percentage.values,
            'Data Type': data_types.values
        })

        # Display the table
        print(missing_data_table)

        # Set up the number of subplots
        num_columns = len(gender_and_marrage_status)
        fig, axes = plt.subplots(1, num_columns, figsize=(15, 6))

        # Loop through each relevant column and plot
        for idx, column in enumerate(gender_and_marrage_status):
            # Calculate the frequency counts
            value_counts = self.data[column].value_counts()
            
            # Create a bar chart in the corresponding subplot
            axes[idx].bar(value_counts.index, value_counts.values, color='skyblue')
            
            # Add titles and labels
            axes[idx].set_title(f'Distribution of {column}')
            axes[idx].set_xlabel(column)
            axes[idx].set_ylabel('Frequency')
            
            # Rotate x-axis labels if necessary
            axes[idx].tick_params(axis='x', rotation=45)

        # Adjust layout
        plt.tight_layout()
        plt.show()

    def plot_premium_vs_claims(self):
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='TotalPremium', y='TotalClaims', hue='PostalCode', data=self.data)
        plt.title('TotalPremium vs TotalClaims by PostalCode')
        plt.xlabel('TotalPremium')
        plt.ylabel('TotalClaims')
        plt.legend(title='PostalCode')
        plt.show()

    def plot_correlation_matrix_for_TotalPremium_and_TotalClaims(self):
        # Select numerical columns
        numeric_columns = ['TotalPremium', 'TotalClaims']
        correlation_matrix = self.data[numeric_columns].corr()

        # Plot the correlation matrix
        plt.figure(figsize=(8, 6))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', vmin=-1, vmax=1)
        plt.title('Correlation Matrix of TotalPremium and TotalClaims')
        plt.tight_layout()
        plt.show()
    
    def analyze_geographic_data(self):
        # Group by Province and aggregate the data
        grouped_data = self.data.groupby(['Province']).agg({
            'CoverType': lambda x: x.value_counts().to_dict(),  # Count occurrences of different cover types
            'TotalPremium': 'mean',                               # Average premium per geographic area
            'make': lambda x: x.value_counts().to_dict()        # Count occurrences of car makes
        }).reset_index()

        # Display the grouped data
        print(grouped_data)

    def plot_cover_type_distribution(self):
        plt.figure(figsize=(12, 6))
        sns.countplot(data=self.data, x='Province', hue='CoverType')
        plt.title('Insurance Cover Type Distribution by Province')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_average_premium_by_province(self):
        plt.figure(figsize=(12, 6))
        sns.barplot(data=self.data, x='Province', y='TotalPremium')
        plt.title('Average Premium by Province')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_car_make_distribution(self):
        plt.figure(figsize=(12, 6))
        sns.countplot(data=self.data, x='Province', hue='make')
        plt.title('Car Make Distribution by Province')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_average_sum_insured_by_make(self):
        plt.figure(figsize=(12, 6))
        sns.barplot(data=self.data, x='make', y='SumInsured', ci=None, palette='Set2')
        plt.title('Average Sum Insured by Car Make')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_boxplots_for_numerical_columns(self):
        # Set up the figure and axes
        plt.figure(figsize=(15, 8))

        # Create box plots for each numerical column
        for i, column in enumerate(self.relevant_numerical_columns):
            plt.subplot(3, 4, i + 1)  # Create a grid of subplots
            sns.boxplot(data=self.data, y=column, palette="coolwarm")
            plt.title(f'Box Plot of {column}')
            plt.tight_layout()

        plt.show()
    
    def plot_correlation_matrix(self):
        correlation_matrix = self.data[self.relevant_numerical_columns].corr()
        plt.figure(figsize=(8, 6))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', vmin=-1, vmax=1)
        plt.title('Correlation Matrix of Numerical Features')
        plt.tight_layout()
        plt.show()

    def export_data(self, output_file):
        self.data.to_csv(output_file, index=False)
        print(f"Data has been exported and saved at: {output_file}")