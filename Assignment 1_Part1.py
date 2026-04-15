import pandas as pd

# Step 1: Load the Excel file
file_path = r'file_path_here.xlsx'  # Replace with your actual file path
xls = pd.ExcelFile(file_path)

# Display available sheet names (optional, for exploration)
print("Available sheets:", xls.sheet_names)

# Step 2: Read the sheet that contains 'Basic Indicators'
# Replace 'Sheet1' with the actual sheet name if different
df_raw = xls.parse('Basic Indicators')

# Display first few rows to verify loading
print("First few rows of the raw data:")
print(df_raw.head())

# Step 3: Extract the 'Basic Indicators' table
# Assuming the table starts after a few header rows, locate it manually or programmatically
# For example, if the table starts at row 5 (index 4), use skiprows
df_table = pd.read_excel(file_path, sheet_name='Basic Indicators', skiprows=6)

# Optional: Drop any empty rows or columns if needed
df_table.dropna(how='all', inplace=True)


# Step 3: Drop the first column (column A)
df_table = df_table.iloc[:, 1:]



# Step 4: Format the Data
# Rename the first column to 'Country Name'
df_table.rename(columns={df_table.columns[0]: 'Country Name'}, inplace=True)

# Rename remaining columns to integers starting from 0
new_columns = ['Country Name'] + list(range(len(df_table.columns) - 1))
df_table.columns = new_columns

# Display formatted table
print("Formatted table:")
print(df_table.head())

# Step 5: Save to CSV
df_table.to_csv(r'file_path_here.csv', index=False, encoding='utf-8-sig')   # Replace with your desired output file path


print("Data saved to basic_indicators_processed.csv")

