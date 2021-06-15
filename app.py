import pandas as pd
from flask import Flask, render_template, redirect, request, session


app = Flask(__name__)

# to be changed manually once a month
# exp_date = '2021-06-24'


def create_url(row):
    final_url = "https://kite.zerodha.com/chart/ext/tvc/NFO-OPT/" + \
        row['tradingsymbol'] + "/" + str(row['instrument_token'])
    return final_url

# filename = r'C:\Users\91956\Desktop\instrument.csv'
# df = pd.read_csv(filename)
df = pd.read_csv('https://api.kite.trade/instruments')
df = df[(df['segment'].str.contains("NFO-OPT") == True)]
df = df[df['instrument_type'].str.contains("CE") == True]
df.drop(df[df['name'] == 'NIFTY'].index, inplace=True)
df.drop(df[df['name'] == 'BANKNIFTY'].index, inplace=True)
df.drop(df[df['name'] == 'FINNIFTY'].index, inplace=True)
ls = (df.expiry.unique())
print(ls[0])
exp_date = ls[0]
df.drop(df[df['expiry'] != exp_date].index, inplace=True)
df['url'] = df.apply(lambda row: create_url(row), axis=1)
# df = pd.read_csv(r'C:\Users\91956\Desktop\a.csv')


@app.route('/')
@app.route('/home', methods=["GET", "POST"])
def home():

    global df

    if request.method == "POST":
        statename = request.form.get("statename")
        statename = str(statename)
        print(statename)
        global date
        date = statename
        print(type(date))

    lis = df.name.unique()
    
    return render_template('index.html',lis = lis)


@app.route('/somework', methods=["GET", "POST"])
def somework():

    global df

    newdf = df
    if request.method == "POST":
        statename = request.form.get("statename")
        statename = str(statename)
        print(statename)    

        newdf = newdf[(newdf['url'].str.contains(statename) == True)]
        lis2 = newdf['url'].tolist()
        return render_template('show.html', lis2=lis2)

    return "hello"


if __name__ == '__main__':
    app.run(debug=True)
