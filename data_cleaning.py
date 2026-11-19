
import pandas as pd

# STEP 1: Read original data
df = pd.read_csv("employees.csv")

print("Original Data:")
print(df)

# STEP 2: Store before cleaning details
before_rows = len(df)
before_missing = df.isnull().sum().sum()
before_duplicates = df.duplicated().sum()

# Make a copy
clean_df = df.copy()


# STEP 3: Handle missing values

# Fix salary: abc becomes missing
clean_df["salary"] = pd.to_numeric(
    clean_df["salary"], errors="coerce"
)

# Fill missing department with mode
clean_df["department"] = clean_df["department"].fillna(
    clean_df["department"].mode()[0]
)

# Fill missing salary with median
clean_df["salary"] = clean_df["salary"].fillna(
    clean_df["salary"].median()
)

# Fill missing city with mode
clean_df["city"] = clean_df["city"].fillna(
    clean_df["city"].mode()[0]
)

# Keep missing date and create a flag
clean_df["date_missing"] = clean_df["joining_date"].isna()


# STEP 4: Fix data types

clean_df["id"] = clean_df["id"].astype(int)

clean_df["joining_date"] = pd.to_datetime(
    clean_df["joining_date"], errors="coerce"
)


# STEP 5: Standardise text

clean_df["name"] = clean_df["name"].str.strip().str.title()

clean_df["department"] = (
    clean_df["department"].str.strip().str.title()
)

clean_df["department"] = clean_df["department"].replace({
    "Hr": "HR",
    "It": "IT"
})

clean_df["city"] = clean_df["city"].str.strip().str.title()


# STEP 6: Remove duplicates

print("\nDuplicates before cleaning:")
print(clean_df.duplicated().sum())

clean_df = clean_df.drop_duplicates()

print("\nDuplicates after cleaning:")
print(clean_df.duplicated().sum())


# STEP 7: Find salary outliers using IQR

Q1 = clean_df["salary"].quantile(0.25)
Q3 = clean_df["salary"].quantile(0.75)

IQR = Q3 - Q1

lower_limit = Q1 - 1.5 * IQR
upper_limit = Q3 + 1.5 * IQR

print("\nLower Limit:", lower_limit)
print("Upper Limit:", upper_limit)

outliers = clean_df[
    (clean_df["salary"] < lower_limit) |
    (clean_df["salary"] > upper_limit)
]

print("\nSalary Outliers:")
print(outliers[["name", "salary"]])

# Keep outliers because they may be genuine salaries


# STEP 8: Before and After Summary

summary = pd.DataFrame({
    "Description": ["Rows", "Missing Values", "Duplicates"],
    "Before Cleaning": [
        before_rows,
        before_missing,
        before_duplicates
    ],
    "After Cleaning": [
        len(clean_df),
        clean_df.isnull().sum().sum(),
        clean_df.duplicated().sum()
    ]
})

print("\nBefore and After Cleaning Summary:")
print(summary)


# STEP 9: Save cleaned data

clean_df.to_csv("clean_data.csv", index=False)

print("\nCleaned data saved successfully!")
