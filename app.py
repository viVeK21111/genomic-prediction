import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import RandomOverSampler, SMOTE, ADASYN
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,mean_absolute_error
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from flask import jsonify,send_file
import pickle
import json
from tensorflow.keras.models import load_model
from joblib import dump,load


df=pd.read_csv("G:\My Drive\ps\data\ddata.csv") 
df=df.drop(columns=['Unnamed: 0'])
x=df.iloc[:,:-2]
y=df.iloc[:,-2]
z=df.iloc[:,-1]
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(x, y)
x_train,x_test,y_train,y_test=train_test_split(X_resampled,y_resampled,random_state=42,test_size=0.33) 
 
model_r=RandomForestClassifier(n_estimators=7,max_depth=9,random_state=42,criterion="gini",max_features='sqrt',max_leaf_nodes=30) 
model_r.fit(x_train,y_train)
s_pred=model_r.predict(x) 
r_pred=model_r.predict(x_test)
print(accuracy_score(y_test,r_pred))
s_pred=list(s_pred)
df_h=pd.DataFrame(df.iloc[:,:-2]) 
df_h['sub']=s_pred 
df_h['sub']=df_h['sub'].astype("category").cat.codes +1  
df_h['height']=z
df_h.columns=df_h.columns.astype(str)   
def Outlier_Treatment(df1,variable):
    global df_final
    percentile25=df1[variable].quantile(0.25)  #q1
    percentile75=df1[variable].quantile(0.75)  #q3
    iqr=percentile75-percentile25
    upper_limit=percentile75+1.5*iqr
    lower_limit=percentile25-1.5*iqr
    df_final = df1[ (df1[variable]>=lower_limit) & (df1[variable]<=upper_limit) ]
Outlier_Treatment(df_h,'height')
xh=df_final.iloc[:,:-1]
yh=df_final.iloc[:,-1] 
X_train,X_test,Y_train,Y_test=train_test_split(xh,yh,random_state=42,test_size=0.33)
from sklearn.preprocessing import MinMaxScaler
mm=MinMaxScaler()
mm.fit(X_train)
X_train=mm.transform(X_train)
X_test=mm.transform(X_test)
from sklearn.ensemble import RandomForestRegressor  
model_rr=RandomForestRegressor(n_estimators=14,max_depth=4,random_state=42,criterion='squared_error')
from sklearn.ensemble import BaggingRegressor
bg_model=BaggingRegressor(base_estimator=model_rr,n_estimators=2,random_state=42)
bg_model.fit(X_train,Y_train)
 
lmc=model_r
lmr=bg_model  
# lmc=load_model('testc.h5') deep learning model(ann) for classification



## flask 

from flask import Flask,redirect,url_for,render_template,request

app=Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/Home')
def Home():
    return render_template('home.html')

@app.route('/pred')
def pred():
    return render_template('index.html')

@app.route('/data')
def data():
    return render_template('data.html')

@app.route('/phylo')
def phylo(): 
    return render_template('datat.html')

@app.route('/about')
def about():
    return render_template('about.html') 

@app.route('/func2') 
def func2():
    return render_template('wlen.html') 

@app.route('/empty')
def empty():
    return render_template('empty.html')

@app.route('/download/<path:filename>')
def download(filename):
    file="G:\\My Drive\\ps\\ui\\download\\"+filename
    return send_file(file,as_attachment=True)

@app.route('/downloadt/<path:filename>')
def downloadt(filename):
    file="G:\\My Drive\\ps\\ui\\download\\"+filename
    return send_file(file,as_attachment=True) 
@app.route('/inv')
def inv():
    return "<h2>Invalid input</h2>"

@app.route('/submit',methods=['POST','GET'])
def submit():
    if request.method=='POST':
        import re
        seq=str(request.form['seq']) 
        if(len(seq)==0):
            return redirect(url_for('empty'))
        alc='ATCG'
        SEQ=re.findall(r'\b\w+\b',seq)  
        sel=str(SEQ)
        sel=sel.replace('[',"")
        sel=sel.replace(']',"")
        sel=sel.replace("'","")
        sel=sel.replace(" ","") 
        sel=list(sel)
        sel=set(sel)
        if(len(SEQ)>1): 
            for i in sel:
                if(i!='A' and i!='T' and i!='C' and i!='G' and i!=','):
                    return redirect(url_for('inv'))
        else:
            for i in sel:
                if(i!='A' and i!='T' and i!='C' and i!='G'):
                    return redirect(url_for('inv'))
        l=len(SEQ)
        flag=0
        p=0
        for i in range(l):
            if(len(SEQ[i])==9): 
                flag=0
            else:
                flag=1
                p=i
                break
        if(flag==0):
            ss=SEQ 
            nuc=['A','T','C','G']
            dicc={'A':1.5,'T':2.5,'C':0.5,'G':0.75}
            encoded=[]
            for i in ss:
                array = np.array(list(i))
                new_arr=np.array([dicc[i] for i in array])
                encoded.append((new_arr))

            enc_dfff=pd.DataFrame(encoded)
            zz=lmc.predict(enc_dfff)  
            id=list(zz)
            enc_dfff['sub']=id
            enc_dfff.columns=enc_dfff.columns.astype(str)
            enc_dfff['sub']=enc_dfff['sub'].astype('category').cat.codes +1 
            res=lmr.predict(enc_dfff)
            res_df=pd.DataFrame()   
            res_df['sequence']=ss
            res_df['subpopulation']=id 
            res_df['height']=res
            rl=res_df.values.tolist() 
            return render_template("dataf.html",rl=rl) 
        else:
            return redirect(url_for('func2'))   
    else:
        return "invalid request" 
if __name__=="__main__":
    app.run(debug=True) 
