# Insurance Data Analysis

This project provides a comprehensive analysis of insurance data, allowing users to explore various aspects such as numerical and categorical variables, geographic distributions, and relationships between different features. The main functionalities are encapsulated in a series of functions designed for data loading, cleaning, visualization, and analysis.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Functions](#functions)
- [License](#license)

## Installation

To run this project, ensure you have Python installed along with the necessary libraries. You can install the required packages using pip:

pip install -r requirments.txt

## Usage
Set the working directory to the location of your data file.
Load the data from a CSV file.
Use the provided functions to analyze and visualize the data.

### Example 
import your_module_name as analysis

#### Set the working directory
analysis.set_working_directory('path/to/your/directory')

#### Load the data
data = analysis.load_data()

#### Check data types
analysis.check_data_types()

#### Describe numerical columns
analysis.describe_numerical_columns()

#### Analyze and visualize
analysis.plot_numerical_analysis()
analysis.analyze_categorical_columns()

## Functions
### set_working_directory(path)
Sets the working directory for file operations.

### load_data()
Loads the data from a CSV file into a Pandas DataFrame.

### check_data_types()
Prints the data types of the columns in the DataFrame.

### describe_numerical_columns()
Describes the numerical columns, providing summary statistics.

### plot_numerical_analysis()
Plots histograms for each numerical column to visualize distributions.

### analyze_categorical_columns()
Analyzes categorical columns and prints frequency tables.

### plot_categorical_analysis(frequency_tables)
Plots bar charts for categorical columns based on frequency tables.

### visualize_missing_values()
Visualizes missing values using a heatmap for better understanding.

### fill_missing_values()
Fills missing values based on specified conditions or methods.

### analyze_marriageStatus_and_gender_columns()
Analyzes the ‘MaritalStatus’ and ‘Gender’ columns for insights.

### plot_premium_vs_claims()
Plots a scatter plot of TotalPremium vs TotalClaims to explore relationships.

### plot_correlation_matrix_for_TotalPremium_and_TotalClaims()
Plots the correlation matrix specifically for TotalPremium and TotalClaims.

### analyze_geographic_data()
Analyzes geographic data by grouping the data by Province.

### plot_cover_type_distribution()
Plots the distribution of insurance cover types by Province.

### plot_average_premium_by_province()
Plots the average premium values by Province.

### plot_car_make_distribution()
Plots the distribution of car makes by Province.

### plot_average_sum_insured_by_make()
Plots the average sum insured by car make.

### plot_boxplots_for_numerical_columns()
Plots box plots for each numerical column to visualize outliers and distributions.

### plot_correlation_matrix()
Plots the correlation matrix for all numerical features in the dataset.

### export_data(output_file)
Exports the modified or analyzed data to a specified CSV file.