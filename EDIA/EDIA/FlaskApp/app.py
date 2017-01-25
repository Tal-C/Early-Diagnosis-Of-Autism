from flask import Flask, render_template, url_for,request,redirect
import requests
#from lxml import html
#import cgi
from flask.helpers import flash
import gc
from UserController import UserController

app = Flask(__name__)

@app.route('/')
def main():
    UserController.insert_user('Gal', '123')
    return render_template('index.html')

@app.route('/item.html', methods=['GET', 'POST'])
def item():
    error = ''
    try:
        if request.method == 'POST':
            attempted_username = request.form['user']
            attempted_password = request.form['passw']
            if attempted_username == '' and attempted_password == '':
                print("you must sing up")
            else:
                print("userName = ", attempted_username)
                print("Password = ", attempted_password)
                resp = UserController.login_page(attempted_username,attempted_password)
                if resp == 0:
                    print("You are now logged in!")
                    return render_template("item.html")
                else:
                    error = "Invalid credetials,try again .!. "
                    print(error)
                    return render_template("index.html",error = error)
                gc.collect()
    except Exception as e:
        return render_template("index.html",error = error)
        #return redirect(url_for('item'))
      # show the form, it wasn't submitted
    return render_template('index.html')
        
if __name__ == "__main__":
    app.run()