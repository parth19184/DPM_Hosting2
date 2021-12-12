from bokeh.models.annotations import Label
from flask import Flask
from flask import request
from flask import render_template,jsonify
from bokeh.embed import components
from bokeh.plotting import figure
import pandas as pd
import numpy as np
import datetime
from datetime import datetime
import pickle
from bokeh.plotting import figure, output_file, show
from bokeh.transform import dodge, linear_cmap
from bokeh.util.hex import hexbin
import json
from werkzeug.datastructures import ImmutableMultiDict

app = Flask(__name__)

@app.route('/',methods = ['GET','POST'])
def index():
    Top = topList()

    if request.method == 'GET':
        allStock = pd.read_csv('NIFTY50_all.csv')
        stock_symbols=allStock.Symbol.unique()
        Top[0] = 'HDFC'
        file1 = 'FinalStockCSV/'+Top[0]+'.csv'
        file2 = 'FinalStockCSV/'+Top[1]+'.csv'
        file3 = 'FinalStockCSV/'+Top[2]+'.csv'
        file4 = 'FinalStockCSV/'+Top[3]+'.csv'
        file5 = 'FinalStockCSV/'+Top[4]+'.csv'
        table = pd.read_csv(file1)
        table1 = pd.read_csv(file2)
        my_data = DataSaved3(table)
        my_data1 = DataSaved3(table1)
        
        x1 = json.dumps(my_data['PosPlot'])
        x2 = json.dumps(my_data['NegPlot'])
        x3 = json.dumps(my_data['NeuPlot'])

        y1 = json.dumps(my_data1['PosPlot'])
        y2 = json.dumps(my_data1['NegPlot'])
        y3 = json.dumps(my_data1['NeuPlot'])
        kwargs ={'x1':x1,'x2':x2,'x3':x3, 'y1':y1,'y2':y2,'y3':y3,
            'files1':Top[0],'files2':Top[1], 'files3':Top[2],'files4':Top[3],'files5':Top[4]}

        return render_template('graph.html', la='TCS', title='Home Page', stock_symbols=stock_symbols, **kwargs)
    else:
        return render_template('graph.html')


@app.route('/details/<st_name>')
def details(st_name):
    allStock = pd.read_csv('NIFTY50_all.csv')
    stock_symbols=allStock.Symbol.unique()
    if(st_name == 'TCS'):
        tb = pd.read_csv('FinalStockCSV/TCS.csv')
        heading = 'TCS'
    elif(st_name == 'Maruti_Suzuki'):
        tb = pd.read_csv('FinalStockCSV/INFOSYS.csv')
        heading = 'Maruti Suzuki'
    else:
        tb = pd.read_csv('FinalStockCSV/TATA_STEEL.csv')
        heading = 'Tata Steel'
    my_data = detailsData(tb)

    PosVal = my_data['val_1']
    NeuVal = my_data['val_2']
    NegVal = my_data['val_3']
    PosPlot = json.dumps(my_data['PosPlot'])
    NegPlot = json.dumps(my_data['NegPlot'])
    NeuPlot = json.dumps(my_data['NeuPlot'])

    kwargs ={'Heading':heading, 'PosVal':PosVal,'NeuVal':NeuVal,'NegVal':NegVal, 'NegPlot':NegPlot, 
        'NeuPlot':NeuPlot, 'PosPlot':PosPlot,'labels':my_data['labs'], 'stock_symbols':stock_symbols}
    return render_template('details.html', **kwargs)

@app.route('/watchList/', methods=['GET','POST'])
def watchList():
    allStocks = pd.read_csv('NIFTY50_all.csv')
    symb = allStocks.Symbol.unique()
    if( request.method == 'GET'):
        return render_template('WL.html', stock_symbols=symb, Stock="Select a Stock")
    elif(request.method == 'POST'):
        req = request.form
        key=""
        value=""
        kwargs={}
        for key,value in req.items():
            fN = value+".csv"
            tb=pd.read_csv("FinalStockCSV"+"/"+fN)
            my_data = detailsData(tb)
            
            PosVal = my_data['val_1']
            NeuVal = my_data['val_2']
            NegVal = my_data['val_3']
            PosPlot = json.dumps(my_data['PosPlot'])
            NegPlot = json.dumps(my_data['NegPlot'])
            NeuPlot = json.dumps(my_data['NeuPlot'])

            kwargs ={'PosVal':PosVal,'NeuVal':NeuVal,'NegVal':NegVal, 'NegPlot':NegPlot, 
                'NeuPlot':NeuPlot, 'PosPlot':PosPlot,'labels':my_data['labs'], 'stock_symbols':symb}
            return render_template('WL.html', **kwargs, Stock=value.replace("_"," "))
            break
        
        return render_template('WL.html', **kwargs)
    else:
        return render_template('WL.html', stock_symbols=symb)


@app.route("/Detail", methods=['GET', 'POST'])
def Detail():
    allStock = pd.read_csv('NIFTY50_all.csv')
    stock_symbols=allStock.Symbol.unique()
    if(request.method =='POST'):
        fileName = request.form['DDst']
        fN = fileName+".csv"
        tb=pd.read_csv("FinalStockCSV"+"/"+fN)
        head_ing = fileName.split("_")
        heading=""
        for head in head_ing:
            heading +=head+" "
        my_data = detailsData(tb)
        
        PosVal = my_data['val_1']
        NeuVal = my_data['val_2']
        NegVal = my_data['val_3']
        PosPlot = json.dumps(my_data['PosPlot'])
        NegPlot = json.dumps(my_data['NegPlot'])
        NeuPlot = json.dumps(my_data['NeuPlot'])

        kwargs ={'Heading':heading, 'PosVal':PosVal,'NeuVal':NeuVal,'NegVal':NegVal, 'NegPlot':NegPlot, 
            'NeuPlot':NeuPlot, 'PosPlot':PosPlot,'labels':my_data['labs'], 'stock_symbols':stock_symbols}
        return render_template('details.html', **kwargs)

@app.route("/Compare/", methods =['POST', 'GET'])
def Compare():
    allStocks = pd.read_csv('NIFTY50_all.csv')
    symb = allStocks.Symbol.unique()
    if( request.method == 'GET'):
        return render_template('compare.html', stock_symbols=symb, heading='Select stock to compare')

    elif(request.method == 'POST'):
        fileName = request.form['DDst']
        my_data = create_positive_bokeh(fileName)
        head_ing = fileName.split("_")
        heading=""
        for head in head_ing:
            heading +=head+" "
        Pos = my_data['Pos']
        labels = my_data['labels']
        labels1 = my_data['labels1']
        closePrice = my_data['close']
        kwargs = {'labels':labels, 'Pos':Pos, 'stock_symbols':symb, 
        'labels1':labels1, 'closePrice':closePrice, 'heading':heading}
        return render_template('compare.html', **kwargs)

    else:
        return render_template('compare.html', stock_symbols=symb, heading='Select stock to compare')


def DataSaved3(table):
        
    import pandas as pd
    from datetime import datetime
    import numpy as np

    def get_datetime(date):
        return datetime.strptime(date[:10], '%Y-%m-%d')

    table["Dt"] = table["Date"].apply(get_datetime)
    grp = table.groupby('Dt')

    date_list = []
    posLen = []
    negLen = []
    neuLen = []
    posfeed = []
    negfeed = []
    neufeed = []
    for i,j in grp:
        x = (str(i)[:10])
        date_list.append(x)
        posLen.append((len(j.loc[j["Analysis"] == "Positive"])))
        negLen.append((len(j.loc[j["Analysis"] == "Negative"])))
        neuLen.append((len(j.loc[j["Analysis"] == "Neutral"])))
        posfeed.append(j["tweet"].loc[j["Analysis"] == "Positive"])
        negfeed.append(j["tweet"].loc[j["Analysis"] == "Negative"])
        neufeed.append(j["tweet"].loc[j["Analysis"] == "Neutral"])
    
    PosPlot=[]
    for i in range(0,len(posfeed)):
        x = {}
        x['label'] = date_list[i]
        x['y'] = posLen[i]
        x['link']=posfeed[i].to_list()
        PosPlot.append(x)

    NegPlot=[]
    for i in range(0,len(negfeed)):
        x ={}
        x['label'] = date_list[i]
        x['y'] = negLen[i]
        x['link']=negfeed[i].to_list()
        NegPlot.append(x)

    NeuPlot=[]
    for i in range(0,len(neufeed)):
        x ={}
        x['label'] = date_list[i]
        x['y'] = neuLen[i]
        x['link']=neufeed[i].to_list()
        NeuPlot.append(x)

    my_data = {'labs':date_list,
    'NeuPlot':NeuPlot,
    'NegPlot':NegPlot,
    'PosPlot':PosPlot
    }
    return  my_data

def detailsData(table):
    import pandas as pd
    from datetime import datetime
    import numpy as np

    def get_datetime(date):
        return datetime.strptime(date[:10], '%Y-%m-%d')

    table["Dt"] = table["Date"].apply(get_datetime)
    grp = table.groupby('Dt')

    date_list = []
    posLen = []
    negLen = []
    neuLen = []
    posfeed = []
    negfeed = []
    neufeed = []
    for i,j in grp:
        x = (str(i)[:10])
        date_list.append(x)
        posLen.append((len(j.loc[j["Analysis"] == "Positive"])))
        negLen.append((len(j.loc[j["Analysis"] == "Negative"])))
        neuLen.append((len(j.loc[j["Analysis"] == "Neutral"])))
        posfeed.append(j["tweet"].loc[j["Analysis"] == "Positive"])
        negfeed.append(j["tweet"].loc[j["Analysis"] == "Negative"])
        neufeed.append(j["tweet"].loc[j["Analysis"] == "Neutral"])

    PosPlot=[]
    for i in range(0,len(posfeed)):
        x = {}
        x['nums'] = i
        x['prod'] = {'val':posLen[i],'link':posfeed[i].to_list()}
        PosPlot.append(x)

    NegPlot=[]
    for i in range(0,len(posfeed)):
        x ={}
        x['nums'] = i
        x['prod'] = {'val':negLen[i],'link':negfeed[i].to_list()}
        NegPlot.append(x)
    
    NeuPlot=[]
    for i in range(0,len(posfeed)):
        x ={}
        x['nums'] = i
        x['prod'] = {'val':neuLen[i],'link':neufeed[i].to_list()}
        NeuPlot.append(x)

    my_data = {'labs':date_list,
    'val_1':posLen,
    'val_2':neuLen,
    'val_3':negLen,
    'NeuPlot':NeuPlot,
    'NegPlot':NegPlot,
    'PosPlot':PosPlot
    }
    return  my_data

def create_positive_bokeh(df):
    import pandas as pd
    from datetime import datetime
    import numpy as np

    def get_datetime(date):
        return datetime.strptime(date[:10], '%Y-%m-%d')
    table = pd.read_csv('FinalStockCSV/'+df+'.csv')
    table["Dt"] = table["Date"].apply(get_datetime)
    grp = table.groupby('Dt')
    
    table1 = pd.read_csv('MarketCSV/'+df+'.csv')
    table1["datetime"] = pd.to_datetime(table1["Date"])
    table1["Strdt"] = table1['datetime'].dt.strftime('%Y-%m-%d')
    k = table1["Strdt"].to_list()
    table1['numeric_values'] = table1['Close Price'].astype(int)
    closing_price_list = table1["numeric_values"].tolist()
    date_list = []
    posLen = []
    for i,j in grp:
        x = (str(i)[:10])
        date_list.append(x)
        posLen.append((len(j.loc[j["Analysis"] == "Positive"])))
    print("type of closing_price_list: ",(date_list), "type of posLen", (posLen))
    dic ={'labels':date_list,
            'Pos':posLen,
            'labels1':k,
            'close':closing_price_list}
    return dic

def topList():
    def get_positive_percentage(stockname):
        df_here = pd.read_csv("FinalStockCSV/{}.csv".format(stockname))
        df_here_groupby = df_here.groupby("Analysis")
        total_cases = len(df_here)
        positive_cases = 0
        for analysis, df in df_here_groupby:
            if analysis == "Positive":
                positive_cases = len(df)
        return (positive_cases/total_cases)*100
    
    positive_percentages_dict = {}
    negative_percentages_dict = {}
    stocklist2 = ["ASIANPAINTS", 'AXIS_BANK', 'BAJAJ_AUTO','BAJAJ_FINANCE', 
    'BAJAJ_FINSERV', 'BHARTI_AIRTEL', 'HCL_TECHNOLOGIES', 'HDFC', 'HDFC_BANK', 'HUL', 
    'ICICI_BANK', 'INDUSIND_BANK', 'INFOSYS', 'ITC', 'KOTAK_MAHINDRA_BANK', 'L&T','3M',
    'MARUTI_SUZUKI', 'NESTLE', 'NTPC', 'ONGC', 'POWER_GRID', 'RELIANCE_IND', 'SBI', 'SUN_PHARMA', 
    'TATA_STEEL', 'TCS', 'TECH_MAHINDRA', 'TITAN', 'ULTRATECH_CEMENT']
    for stock in stocklist2:
        positive_percentages_dict[stock] = get_positive_percentage(stock)
    sorted_positive_percentages = sorted(positive_percentages_dict.items(), key=lambda x: x[1])
    topList = []
    for i in sorted_positive_percentages[-1:-6:-1]:
        topList.append(i[0])
    return (topList)

if __name__ == '__main__':
    app.run(debug=True)