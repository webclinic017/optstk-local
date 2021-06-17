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
# df = df[df['instrument_type'].str.contains("CE") == True]
df.drop(df[df['name'] == 'NIFTY'].index, inplace=True)
df.drop(df[df['name'] == 'BANKNIFTY'].index, inplace=True)
df.drop(df[df['name'] == 'FINNIFTY'].index, inplace=True)
ls = (df.expiry.unique())
print(ls[0])
exp_date = ls[0]
df.drop(df[df['expiry'] != exp_date].index, inplace=True)
df['url'] = df.apply(lambda row: create_url(row), axis=1)
# df.to_csv(r'C:\Users\91956\Desktop\a.csv')


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


@app.route('/get_strikes', methods=["GET", "POST"])
def somework():

    global df

    ce = df
    pe = df
    if request.method == "POST":
        statename = request.form.get("statename")
        statename = str(statename)
        print(statename)    


        ce = ce[(ce['url'].str.contains(statename) == True)
                & (ce['instrument_type'] == 'CE')]
        ce_list = ce['url'].tolist()

        pe = pe[(pe['url'].str.contains(statename) == True)
                & (pe['instrument_type'] == 'PE')]
        pe_list = pe['url'].tolist()
        
        return render_template('show.html', ce_list=ce_list,pe_list=pe_list)

    return "hello"


if __name__ == '__main__':
    app.run(debug=True)
