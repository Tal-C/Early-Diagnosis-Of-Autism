
from flask import Flask, render_template, url_for,request,redirect
app = Flask(__name__)


@app.route('/')
def main():
    return render_template('item.html')

@app.route('/item.html', methods=['GET', 'POST'])
def item():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('index'))
      # show the form, it wasn't submitted
    return render_template('item.html')
        

if __name__ == "__main__":
    app.run()