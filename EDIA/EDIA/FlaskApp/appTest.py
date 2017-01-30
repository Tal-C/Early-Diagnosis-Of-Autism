from flask import Flask, render_template, url_for,request,redirect
import requests
from flask.helpers import flash
import gc
from UserController import UserController

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

def get_data():
    response = requests.get("http://localhost:5000")
    print("*************************************************\n",response)
    print("**************************************************")
    return response

#@app.route('/item.html', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    error = ''
    try:
        if request.method == 'POST':
            attempted_username = request.form['user']
            attempted_password = request.form['passw']
            resp = UserController.login_page(attempted_username,attempted_password)
            if resp == 0:
                print("You are now logged in!")
                return render_template("item.html")
            else:
                error = "Invalid credetials,try again .!. "
                print(error)
                return render_template("index.html",response = get_data())
            gc.collect()
    except Exception as e:
        print(e)
        return render_template("index.html")
        #return redirect(url_for('item'))
      # show the form, it wasn't submitted
    return render_template('index.html')


@app.route('/signup.html', methods=['GET', 'POST'])        
def signup():
    return

if __name__ == "__main__":
    app.run()