from datetime import timedelta
from faucet import Faucet
from flask import Flask, render_template, request, flash, redirect, url_for
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv('./.env')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'wthisthis?'

RECAPTCHA_SECRET = os.environ['RECAPTCHA_SECRET_KEY']
faucet = Faucet('./faucet_config.json', os.environ['MONGODB_URI'])


def is_human(captcha_response):
    """ Validating recaptcha response from google server
        Returns True captcha test passed for submitted form else returns False.
    """
    secret = RECAPTCHA_SECRET
    payload = {'response': captcha_response, 'secret': secret}
    response = requests.post(
        "https://www.google.com/recaptcha/api/siteverify", payload)
    response_text = json.loads(response.text)
    return response_text['success']


def validate_form_request(request, send_flash=True):
    addr_valid = request.form['valid-addr']
    captcha_response = request.form['g-recaptcha-response']
    human = is_human(captcha_response)

    if not (human & (addr_valid == 'true')):
        if send_flash:
            if not human:
                flash('Invalid captcha, try again.')
            if addr_valid == 'false':
                flash('Invalid wallet address.')
        return False
    return True

def claim(
        request,
        coin,
        net,
        form_img,
        form_title,
        form_input_label,
        form_btn_text):
    if request.method == 'POST':
        if validate_form_request(request, coin):
            claimed = faucet.claim(request.remote_addr,
                                   request.form['wallet-addr'], coin, net)
            if claimed[0] == True:
                return render_template('result.html', claimed=True, coin=coin, claim_amount=claimed[1], wallet_addr=request.form['wallet-addr'], threshold=faucet.get_config(coin)['withdraw_threshold'], balance=faucet.wallet_info(request.form['wallet-addr'], coin, net).balance)
            return render_template('result.html', time_left=str(timedelta(seconds=claimed[1])))
        return redirect(url_for(coin))

    return render_template(
        'claim.html',
        coin=coin,
        form_img=form_img,
        form_title=form_title,
        form_input_label=form_input_label,
        form_btn_text=form_btn_text
    )


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/btc.html/', methods=['POST', 'GET'])
def btc():
    return claim(
        request=request,
        coin='btc',
        net='mainnet',
        form_img=url_for('static', filename='images/btc.png'),
        form_title='Get Free Bitcoins',
        form_input_label='Bitcoin wallet address',
        form_btn_text='Get Bitcoins'
    )


@app.route('/eth.html/', methods=['POST', 'GET'])
def eth():
    return claim(
        request=request,
        coin='eth',
        net='mainnet',
        form_img=url_for('static', filename='images/eth.png'),
        form_title='Get Free Ethereum',
        form_input_label='Ethereum wallet address',
        form_btn_text='Get Ethereum'
    )


@app.route('/doge.html/', methods=['POST', 'GET'])
def doge():
    return claim(
        request=request,
        coin='doge',
        net='mainnet',
        form_img=url_for('static', filename='images/doge.png'),
        form_title='Get Free Dogecoins',
        form_input_label='Dogecoin wallet address',
        form_btn_text='Get Dogecoins'
    )


@app.route('/xmr.html/', methods=['POST', 'GET'])
def xmr():
    return claim(
        request=request,
        coin='xmr',
        net='mainnet',
        form_img=url_for('static', filename='images/xmr.png'),
        form_title='Get Free Monero',
        form_input_label='Monero wallet address',
        form_btn_text='Get Monero'
    )


if __name__ == '__main__':
    app.run(debug=True)
