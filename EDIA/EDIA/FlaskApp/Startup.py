from flask import Flask, render_template, url_for,request,redirect
import requests
import gc
import UserController
import time
import numpy as np

app = Flask(__name__)
##Load the first page
@app.route('/')
def main():
    return render_template('index.html')

##--------SignIn Functionality from html page----------##
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    """ get user name and password from sign in fields
    send them to Controller to validate and return SignIn page on success 
    or back to Index on Fail.
    Additionally, show the user data on his personal area."""
    error = ''
    try:
        if request.method == 'POST':
            username = str(request.form['user'])
            password = str(request.form['passw'])
            userptr = UserController.User_Controller()
            resp = userptr.signin_handler(username,password)
            #Check type of user
            if resp == 404:#User not found
                error = 'Wrong username/password'
                return render_template("index.html",signin = error)

            elif resp == 100:
                error = 'Wrong UserName/Password format'
                return render_template("index.html",signin = error)

            else:#resp = 0 - OK
                #Insert data to the page Welcome {Name} + Data To the Table
                data = np.array(resp)#convert to numpy array
                return render_template("signin.html",signin=data)
                
            gc.collect()
        else:
            return render_template("index.html")
    except Exception as e:
        return render_template("index.html",error = error)
    #return render_template('index.html')
##--------Sign Up Functionality from html page----------##
@app.route('/signup', methods=['GET', 'POST'])
def signup():
     """ Get user's input of all his data to sign him up.
     First of all chechks two inserted passwords and then go to DataAccess Layer to validate and insert DB
     """
     error = ''
     try:
        if request.method == 'POST':
            uname = str(request.form['uname'])
            email = str(request.form['email'])
            pswdf = str(request.form['pswdf'])
            pswds = str(request.form['pswds'])
            
            
            if(pswdf != pswds):
                error = 'Your passwords are not equal!'
                return render_template("index.html",signup = error)
                #return error message
            else:
                fname = str(request.form['fname'])
                lname = str(request.form['lname'])
                address = "" if request.form['address'] == None else str(request.form['address'])
                number = str(request.form['number'])
                city = str(request.form['city'])
                zipCode = str(request.form['zip'])
                comments = str(request.form['comment'])

                userptr = UserController.User_Controller()
                #return values of errors!
                resp = userptr.signup_handler(uname,pswdf,email,fname,lname,number,address,city,zipCode,comments)

            gc.collect()
        else:
            return render_template("index.html")
     except Exception as e:
         return render_template("item.html",error = error)
##--------upload video Functionality from html page----------##

#def upload_video():
#    return



##--------buildRequest Functionality from html page----------##
@app.route('/buildRequest', methods=['GET', 'POST'])
def buildRequest():
    #Integration
    """ get the request from client with all data
        and the video, sends the video to VideoController to check validation """

    #get the video

    #send the video to VideoController - check the size and qulity of the video
    #and send to Main(video)
    #Main(object)#object = video
    
    print("Hello to build Request")
    return render_template('index.html')
#def upload_video():
#    print("Hello from upload a video")
#    return        
##--------------ITEM-FUNCS-----------------------------------##
@app.route('/logout')
def logout():
    time.sleep(5)
    return render_template("index.html")



if __name__ == "__main__":
    app.run()