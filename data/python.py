import pandas as pd
df = pd.read_csv("flat_vs_hierarchical_companies_performance.csv")
print(df.dtypes)  # Check the data types of the columns
df = df.astype('int')  # Convert all columns to Python integers
df['Objective'] = df['Objective'].astype(int)
