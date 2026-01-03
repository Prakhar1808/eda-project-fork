import pandas as pd

data = {
    "name" : ["Alice", "Bob", "Charlie" , "David" , "Eva"],
    "age" : [25, 30, 35 , 18, 22],
    "city" : ["New York", "Los Angeles", "Chicago" , "Houston" , "Phoenix"]
}

df = pd.DataFrame(data)
print(df)

df. to_csv("save_output.csv")  # save dataframe to csv file and create a file named save_output.csv 

# to display custom rows of data we use head() and tail() functions
df.head(2)  # display first 2 rows of data
df.tail(2)  # display last 2 rows of data
print (df.head(2))
print("---------------")
print (df.tail(2))

print(df['name'])
print(df[df['age'] > 25])  # to print rows where age is greater than 25