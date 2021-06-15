import pandas as pd


def create_url(row):
    final_url = "https://kite.zerodha.com/chart/ext/tvc/NFO-OPT/" + \
        row['tradingsymbol'] + "/" + str(row['instrument_token'])
    return final_url

# filename = r'C:\Users\91956\Desktop\instrument.csv'
# df = pd.read_csv(filename)
# df = pd.read_csv('https://api.kite.trade/instruments')
# df = df[(df['segment'].str.contains("NFO-OPT") == True)]
# df = df[df['instrument_type'].str.contains("CE") == True]
# df.drop(df[df['name'] == 'NIFTY'].index, inplace=True)
# df.drop(df[df['name'] == 'BANKNIFTY'].index, inplace=True)
# df.drop(df[df['expiry'] != '2021-06-24'].index, inplace=True)
# df['url'] = df.apply(lambda row: create_url(row), axis=1)
# df.to_csv(r'C:\Users\91956\Desktop\a.csv')


# df = pd.read_csv(r'C:\Users\91956\Desktop\a.csv')
# lis = df.name.unique()
# df = df[(df['url'].str.contains("AARTIIND") == True)]
# lis2 = df['url'].tolist()
# print(lis2)
# print(type(lis[0]))

s1 = "https://kite.zerodha.com/chart/ext/tvc/NFO-OPT/MINDTREE21JUN1200CE/24558850"

print(s1.replace(s1[0:s1.find("JUN")+3],"")[:-9])























# create dataframe of option links
# filename = r'C:\Users\91956\Desktop\instrument.csv'
# df = pd.read_csv('https://api.kite.trade/instruments')
# df = pd.read_csv(filename)
# df = df[(df['segment'].str.contains("NFO-OPT") == True)]

# filename = r'C:\Users\91956\Desktop\a.csv'
# df = pd.read_csv(filename)
# df.drop(df[df['expiry'] != '2021-06-24'].index, inplace=True)
# df.to_csv(r'C:\Users\91956\Desktop\a.csv')
# # print(df['expiry'])























 
