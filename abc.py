import pandas as pd


filename = r"C:\Users\91956\Desktop\abcd.csv"
statename = "hdfcbank"
statename = statename.upper()
df = pd.read_csv(filename)
ans = df.loc[df['tradingsymbol'] == statename]
ans = ans['url'].tolist()
ans = ans[0]
print(ans)

# # ans = df.loc[df['url'].str.contains(statename, case=False)]
# # ans.drop(ans[ans['tradingsymbol'] != statename].index, inplace=True)
# lis = ans['url'].tolist()
# print(lis)
