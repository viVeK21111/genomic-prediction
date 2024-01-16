import pandas as pd
import numpy as np
from flask import jsonify
import json
df=pd.read_csv("G:\My Drive\ps\data\ddata.csv") 
from tensorflow.keras.models import load_model
from joblib import dump,load 
lmr=load("G:\\My Drive\\ps\\neural_networks\\modelr.joblib")
lmc=load_model("G:\\My Drive\\ps\\neural_networks\\modelc.h5") 
subb=pd.DataFrame(pd.get_dummies(df['subpopulation'])).columns
subb=list(subb) 
import random
nuc=['A','T','C','G']
ss=[]


from flask import Flask,redirect,url_for,render_template,request

app=Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/func1/<seq>') # decorator
def func1(seq):
    ss=seq.split(',')
    dicc={'A':1.5,'T':2.5,'C':0.5,'G':0.75}
    encoded=[]
    for i in ss:
        array = np.array(list(i))
        new_arr=np.array([dicc[i] for i in array])
        encoded.append((new_arr))

    enc_dfff=pd.DataFrame(encoded)
    zz=lmc.predict(enc_dfff)
    zz=pd.DataFrame(zz)
    id=zz.idxmax(axis=1)

    enc_dfff['9']=id
    id=list(id) 
    enc_dfff.columns=enc_dfff.columns.astype(str)
    res=lmr.predict(enc_dfff)
    res_df=pd.DataFrame()
    lis=list()
    for i in id:
        lis.append(subb[i])   
    res_df['sequence']=ss
    res_df['subpopulation']=lis
    res_df['height']=res
    rl=res_df.values.tolist() 
    return render_template("dataf.html",rl=rl) 
 
@app.route('/func2/<w>') 
def func2(w):
    return "<h2> your entered sequence is of wrong length </h2>"+ """we 
     currently accept the sequences which are of only length 9, """ +w

@app.route('/submit',methods=['POST','GET'])
def submit():
    if request.method=='POST':
        seq=str(request.form['seq'])
        SEQ=seq.split(',') 
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
            return redirect(url_for('func1',seq=seq))
        else:
            return redirect(url_for('func2',w=SEQ[p]))   
    else:
        return "invalid request" 
if __name__=="__main__":
    app.run(debug=True) 