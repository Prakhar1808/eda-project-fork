import pandas as pd

# read data from csv file from dataframe
df = pd.read_csv("D:\GIT WORK AND STUDY\ML(PYTHON)\MACHINE-LEARNING\learning\pandas\gold_data.csv")
# df = name that we can give by ourselves
# pd.read_csv() = function to read csv file
print(df)

df.head(10)  # display first 2 rows of data
df.tail(10)  # display last 2 rows of data
print (df.head(10))
print("---------------")
print (df.tail(10))

# to print info of the dataframe
print(df.info())

# describe() function is used to see some statistical data like mean, std, min, max, percentiles
print(df.describe()) 

# to print the columns of the dataframe
print(df.columns)
# to print the shape of the dataframe
print(df.shape)
# to print specific column data
print(df['Date'])  # to print Date column data
print(df['Price'])  # to print Price column data