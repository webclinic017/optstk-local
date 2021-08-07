import pandas as pd
from flask import Flask, render_template, redirect, request, session
import datetime

app = Flask(__name__)

df = pd.read_csv('https://api.kite.trade/instruments')


# find near month expiry date and month  
dic  = {
    "01" : "JAN",
    "02" : "FEB",
    "03" : "MAR",
    "04" : "APR",
    "05" : "MAY",    
    "06" : "JUN",
    "07" : "JUL",
    "08" : "AUG",
    "09" : "SEP",
    "10" : "OCT",
    "11" : "NOV",
    "12" : "DEC",    
}

dff = df
dff = dff[(dff['segment'].str.contains("NFO-FUT") == True)]
dff.drop(dff[dff['name'] != 'NIFTY'].index, inplace=True)
lis = dff['expiry'].to_list()
d_lis = []
for i in lis:
    d_lis.append(datetime.datetime.strptime(i,'%Y-%m-%d'))

exp_date_zerodha = min(d_lis).strftime('%Y-%m-%d')
month = exp_date_zerodha[5:7]
month_str = dic[month]



def create_url_for_options(row):
    final_url = "https://kite.zerodha.com/chart/ext/tvc/NFO-OPT/" + \
        row['tradingsymbol'] + "/" + str(row['instrument_token'])
    return final_url

def create_url_for_spot(row):
    final_url = "https://kite.zerodha.com/chart/ext/tvc/NSE/" + \
        row['tradingsymbol'] + "/" + str(row['instrument_token'])
    return final_url

def create_url_for_futures(row):
    final_url = "https://kite.zerodha.com/chart/ext/tvc/NFO-FUT/" + \
        row['tradingsymbol'] + "/" + str(row['instrument_token'])
    return final_url


spot_df = df
spot_df = spot_df[(spot_df['instrument_type'].str.contains("EQ") == True)]
spot_df.drop(spot_df[spot_df['segment'] == 'BCD'].index, inplace=True)
spot_df.drop(spot_df[spot_df['segment'] == 'BSE'].index, inplace=True)
spot_df.drop(spot_df[spot_df['segment'] == 'INDICES'].index, inplace=True)
spot_df['url'] = df.apply(lambda row: create_url_for_spot(row), axis=1)
spot_df.to_csv("abcd.csv")


# df1 is for futures
df1 = df
df = df[(df['segment'].str.contains("NFO-OPT") == True)]
df.drop(df[df['name'] == 'NIFTY'].index, inplace=True)
df.drop(df[df['name'] == 'BANKNIFTY'].index, inplace=True)
df.drop(df[df['name'] == 'FINNIFTY'].index, inplace=True)
ls = (df.expiry.unique())
print(ls[0])
# exp_date = ls[0]
df.drop(df[df['expiry'] != exp_date_zerodha].index, inplace=True)
df['url'] = df.apply(lambda row: create_url_for_options(row), axis=1)



df1 = df1[(df1['segment'].str.contains("NFO-FUT") == True)]
df1.drop(df1[df1['expiry'] != exp_date_zerodha].index, inplace=True)
df1['url'] = df1.apply(lambda row: create_url_for_futures(row), axis=1)



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
        
        return render_template('show.html', ce_list=ce_list,pe_list=pe_list,month = month_str)

    return "hello"


@app.route('/get_fut', methods=["GET", "POST"])
def fut():

    global df1

    df2 = df1
    
    statename = request.args.get('statename')
    print(statename)
    statename = statename.upper()    
    ans = df2.loc[df2['name'] == statename]
    ans = ans['url'].tolist()
    ans = ans[0]
    req_url = ans

    return redirect(req_url)

    return "hello"



@app.route('/get_spot', methods=["GET", "POST"])
def spot():

    global spot_df

    df2 = spot_df
    
    statename = request.args.get('statename')
    print(statename)
    statename = statename.upper()
   
    ans = df2.loc[df2['tradingsymbol'] == statename]
    ans = ans['url'].tolist()
    print("created ans is ")
    print(ans)
    ans = ans[0]
    req_url = ans

    return redirect(req_url)

    return "hello"


@app.route('/get_opt', methods=["GET", "POST"])
def opt():
    global df

    ce = df
    pe = df
  
    statename = request.args.get('statename')
    print(statename)
    
   
    ce = ce[(ce['url'].str.contains(statename) == True)
            & (ce['instrument_type'] == 'CE')]
    ce_list = ce['url'].tolist()

    pe = pe[(pe['url'].str.contains(statename) == True)
            & (pe['instrument_type'] == 'PE')]
    pe_list = pe['url'].tolist()

    return render_template('show.html', ce_list=ce_list, pe_list=pe_list,month = month_str)




@app.route('/req_opt', methods=["GET", "POST"])
def reqopt():
    global df

    ce = df
    pe = df
  
    statename = request.args.get('statename')
    ltp = request.args.get('ltp')
    print(statename)
    print(ltp)
    
    ltp = int(float(ltp))
   
    ce = ce[(ce['url'].str.contains(statename) == True)
            & (ce['instrument_type'] == 'CE')]
    # ce_list = ce['url'].tolist()
    idx = ce['strike'].lt(ltp).argmin()
    out = ce['url'].iloc[max(idx-4, 0):min(idx+4, len(df))]
    ce_list = out.tolist()
    print(ce_list)

    pe = pe[(pe['url'].str.contains(statename) == True)
            & (pe['instrument_type'] == 'PE')]
    # pe_list = pe['url'].tolist()
    idx = pe['strike'].lt(ltp).argmin()
    out = pe['url'].iloc[max(idx-4, 0):min(idx+3, len(df))]
    pe_list = out.tolist()
    print(pe_list)

    return render_template('show.html', ce_list=ce_list, pe_list=pe_list,month = month_str)


if __name__ == '__main__':
    app.run(debug=True)


# http://localhost:5000/abcd?user = 123
