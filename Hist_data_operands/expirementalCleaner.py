import pandas as pd

# Let's create a sample DataFrame
df = pd.DataFrame({
    'A': [1, 2, 'a', 4, 5],
    'B': [999, 999, 999, 999, 999],
    'C': [1.2, 2.3, 3.4, 4.5, 5.6],
    'D': ['x', 'y', 'z', 'x', 'y']
})

print("Original DataFrame:")
print(df)

# Remove rows with non-numerical values
df = df[pd.to_numeric(df['A'], errors='coerce').notnull()]

def check(n):
    if type(n) == int or type(n) == float:
        return str(int(n)) == '9' * len(str(int(n)))
    return False

# Remove columns where most of the values are 9's
threshold = 0.8  # change this to adjust the threshold
df = df.loc[:, df.apply(lambda x: (x.apply(check)).sum() / len(x) < threshold, axis=0)]

print(df)

print("\nCleaned DataFrame:")
