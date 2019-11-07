from flask import render_template
from flask import Flask
import maindata

app = Flask(__name__)

#@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Swapnil'}
    return render_template('index.html', title='Home', user=user)

@app.route('/')
def analysis():
    start = '2008-01-01'
    end = '2019-01-01'
    company_list = ['BALRAMCHIN', 'BANDHANBNK', 'BANKBARODA', 'BANKINDIA', 'MAHABANK']

    x = maindata.get_effitient_frontier(start,end,company_list)

    x['min_variance_portfolio'].map(lambda n: '{:,.2%}'.format(n))
    x['min_variance_portfolio'].map(lambda n: '{:,.2%}'.format(n))
    x['min_variance_portfolio'].map(lambda n: '{:,.2%}'.format(n))
    columns = ['min_variance_portfolio','max_sharpe_portfolio','max_returns_portfolio']
    x[columns] = x[columns].applymap(lambda x: "{0:.2f}%".format(x*100))


    x.style.format({'min_variance_portfolio': "{:.2f}",'max_sharpe_portfolio': "{:.2f}",'max_returns_portfolio': "{:.2%}"})
    return render_template("analysis.html",  data=x)


if __name__=="__main__":
    app.run(port=8080,debug=True)

