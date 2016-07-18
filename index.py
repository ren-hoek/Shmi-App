from flask import Flask, render_template, request, flash
from forms import TrustForm, DiagForm
import pandas as pd
import numpy as np

app = Flask(__name__)

app.secret_key = 'This stops a CSRF attack!'

diag_data=pd.read_csv('DiagData.csv')
diag_names=pd.read_csv('DiagNames.csv')
shmi=pd.merge(diag_data, diag_names, on='diagnosis_group', how='inner')

provider = shmi.provider_name.value_counts()

diagnosis = diag_names['diagnosis_group_name']

shmi['numeric_obs'] = 0
shmi.ix[shmi.observed=="*",'numeric_obs'] = np.nan
shmi.ix[shmi.observed!="*",'numeric_obs'] = shmi.observed

shmi['numeric_obs'] = shmi['numeric_obs'].astype('float')

shmi['shmi'] = shmi.numeric_obs/shmi.expected

shmi = shmi.drop('numeric_obs', 1)



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/table', methods=['GET', 'POST'])
def table():

    form = TrustForm()
    form.hosp_drop.choices = (
        [(hosp, hosp) for hosp in provider.index]
    )

    select = []

    if request.method == 'POST':
        trust = form.hosp_drop.data
        sel=shmi[shmi.provider_name==trust][['diagnosis_group_name','spells','observed','expected','shmi']]
        select = sel.values.tolist()


    return render_template('table.html'
     ,results=select
     ,form=form)

@app.route('/graph', methods=['GET', 'POST'])
def graph():
    form = DiagForm()
    form.diag_drop.choices = (
        [(diag, diag) for diag in diagnosis]
    )

    select = []

    if request.method == 'POST':
        disease = form.diag_drop.data
        sel=shmi[shmi.diagnosis_group_name==disease][['provider_name','spells','observed','expected','shmi']]
        select = sel.values.tolist()


    return render_template('graph.html',results=select,form=form)

if __name__ == '__main__':
    app.run(debug=True)
