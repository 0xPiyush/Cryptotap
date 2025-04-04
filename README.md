# Cryptotap - Cryptocurrency Faucet

Cryptotap is a web application built with Flask that functions as a cryptocurrency faucet. It allows users to claim small amounts of various cryptocurrencies (Bitcoin, Ethereum, Dogecoin, Monero) after completing a reCAPTCHA verification.

## Features

- **Multi-Coin Support:** Dispenses BTC, ETH, DOGE, and XMR.
- **Claim Cooldown:** Users must wait a configurable amount of time between claims (based on IP address).
- **Withdrawal Threshold:** Claimed coins accumulate in a user's balance and are sent when a threshold is met (Note: Withdrawal logic is not implemented in the provided code, only balance tracking).
- **reCAPTCHA Verification:** Protects against bots using Google reCAPTCHA v2.
- **Database Integration:** Uses MongoDB to store user claim timestamps and wallet balances.
- **Configurable:** Faucet parameters (timeouts, thresholds, prize amounts) are set in a JSON configuration file.

## Tech Stack

- **Backend:** Python, Flask
- **Database:** MongoDB with MongoEngine ODM
- **Frontend:** HTML, CSS, JavaScript, Bootstrap, jQuery, Anime.js, Vanilla-tilt.js
- **Verification:** Google reCAPTCHA v2
- **WSGI Server:** Gunicorn (as per Procfile)

## Project Structure

```
.
├── .env                  # Environment variables (MongoDB URI, reCAPTCHA secret)
├── .gitignore            # Git ignore rules
├── Procfile              # Heroku deployment configuration
├── README.md             # This file
├── app.py                # Main Flask application logic, routes
├── faucet.py             # Faucet core logic (claiming, timing, config)
├── faucet_config.json    # Configuration for different coins
├── models                # MongoDB data models (MongoEngine)
│   ├── Users.py
│   └── Wallets.py
├── requirements.txt      # Python dependencies
├── static                # Static assets (CSS, JS, Images)
│   ├── images
│   ├── js
│   └── styles
└── templates             # HTML templates (Jinja2)
    ├── claim.html
    ├── index.html
    └── result.html
```

## Setup and Installation

1.  **Prerequisites:**

    - Python 3.x
    - pip
    - MongoDB instance (local or cloud like MongoDB Atlas)
    - Google reCAPTCHA v2 Site Key and Secret Key

2.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd Cryptotap
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the project root and add your MongoDB connection string and reCAPTCHA secret key:

    ```dotenv
    # .env
    RECAPTCHA_SECRET_KEY=YOUR_RECAPTCHA_V2_SECRET_KEY
    MONGODB_URI=YOUR_MONGODB_CONNECTION_STRING_INCLUDING_DB_NAME
    ```

    - Replace `YOUR_RECAPTCHA_V2_SECRET_KEY` with your actual reCAPTCHA secret key.
    - Replace `YOUR_MONGODB_CONNECTION_STRING_INCLUDING_DB_NAME` with your MongoDB connection URI (e.g., `mongodb://localhost:27017/faucet` or a MongoDB Atlas URI).

5.  **Update reCAPTCHA Site Key:**
    In `templates/claim.html`, replace the `data-sitekey` value in the `div` with class `g-recaptcha` with your actual reCAPTCHA _site_ key.

    ```html
    <!-- filepath: templates\claim.html -->
    <!-- ...existing code... -->
    <div class="g-recaptcha" data-sitekey="YOUR_RECAPTCHA_V2_SITE_KEY"></div>
    <!-- ...existing code... -->
    ```

6.  **Configure Faucet Settings:**
    Modify `faucet_config.json` to set claim timeouts (in seconds), withdrawal thresholds, and prize ranges for each supported coin.

7.  **Run the application:**
    ```bash
    python app.py
    ```
    The application will be accessible at `http://127.0.0.1:5000/` by default.

## Deployment

The included `Procfile` suggests using Gunicorn for deployment:

```
web: gunicorn app:app
```

This is suitable for platforms like Heroku. Ensure your deployment environment has the necessary environment variables (`MONGODB_URI`, `RECAPTCHA_SECRET_KEY`) set.
