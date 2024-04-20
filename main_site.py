from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('main_menu.html')


@app.route('/clothes')
def clothes():
    return render_template('main_menu.html')


@app.route('/login')
def login():
    return


@app.route('/clothes/gosha_adidas_black_longsleeve')
def clothes_gosha_black():
    return


@app.route('/clothes/gosha_adidas_red_longsleeve')
def clothes_gosha_red():
    return


@app.route('/clothes/gosha_longsleeve_renessans')
def clothes_gosha_longsleeve_renessans():
    return


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="8080")
