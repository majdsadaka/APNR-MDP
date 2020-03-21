from flask import Flask
import json
from flask import Flask, flash, redirect, render_template, request, session, abort
import os

app = Flask(__name__)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return redirect("/record")

@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == '123321123' and request.form['username'] == 'robertfarha':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()
@app.route('/save',methods=['POST'])
def save():
    if request.form['Modif']=="Add":
        if request.form['CarNumber']!="":
            def write_json(data, filename='reg.json'): 
                with open(filename,'w') as f: 
                    json.dump(data, f, indent=4) 
           
            with open('reg.json') as json_file: 
                data = json.load(json_file) 
      
                temp = data
                
                if(request.form['CarNumber'] in temp.keys()):
                    flash('Number already exists')
                    return redirect("/record")
                
                temp[request.form['CarNumber']] ={"First Name":request.form['Fn'], 
                     "Last Name": request.form['Ln'], 
                     "Phone Number": request.form['Pn'],
                     "Car Number":request.form['CarNumber']
                         } 
      
                write_json(temp)
        else:
            flash('Please enter a valid number')
        return redirect("/record")
    else:
        with open('reg.json', 'r') as data_file:
            data = json.load(data_file)
            
        if(request.form['CarNumber'] in data):
            del data[request.form['CarNumber']]
            with open('reg.json', 'w') as data_file:
                json.dump(data, data_file)
            return redirect("/record")
        else:
            flash('Number doesnt exist')
            return redirect("/record")
        
        
@app.route('/record',methods=['POST','GET'])
def record():      
    with open('reg.json') as json_file: 
                data = json.load(json_file)       
                records = data
                numbers=[]
                colnames=[]
                for num in records.keys():
                    numbers.append(num)
                for kw in records[numbers[0]].keys():
                        colnames.append(kw)
                return render_template('record.html', records=records, colnames=colnames, numbers=numbers)

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='localhost', port=5000)