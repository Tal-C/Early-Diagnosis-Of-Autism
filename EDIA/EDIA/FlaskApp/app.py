from flask import Flask, render_template
app = Flask(__name__)


def main():
    return render_template('Index.html')



if __name__ == "__main__":
    app.run()