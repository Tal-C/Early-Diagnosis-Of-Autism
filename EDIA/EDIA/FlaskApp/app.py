from flask import Flask, render_template, url_for,request,redirect
import requests
import gc
from UserController import UserController
import sys


app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error = ''
    try:
        if request.method == 'POST':
            attempted_username = request.form['user']
            attempted_password = request.form['passw']
            if attempted_username == '' and attempted_password == '':
                print("you must sing up")
            else:
                print(str(attempted_password))
                resp = UserController.login_page(str(attempted_username),str(attempted_password))
                if resp == 0:
                    print("You are now logged in!")
                    return render_template("item.html")
                else:
                    error = "Invalid credetials,try again .!. "
                    print(error)
                    return render_template("index.html",error = error)
                gc.collect()
    except Exception as e:
        return render_template("item.html",error = error)
    return render_template('index.html')

@app.route('/buildRequest', methods=['GET', 'POST'])
def buildRequest():
    print("Hello to build Request")
    return render_template('index.html') 
       
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    print("Hello Sign Up")
    return render_template('item.html')

if __name__ == "__main__":
    app.run(port=2000)