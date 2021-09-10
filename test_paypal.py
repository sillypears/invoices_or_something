import os, sys
import argparse
import logging
from configs.config import app_config
from configs.order import Order
from random import randint

from api import paypal

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--env', dest='env', required=True, help='Set environment')
    args = parser.parse_args()
    config = app_config[args.env]
    if not os.path.exists('logs'):
        os.mkdir('logs')
    logging.basicConfig(filename='logs/test_paypal.log', encoding='utf-8', level=logging.DEBUG if config.DEBUG else logging.INFO)
    
    logging.info("Getting Token")
    token = paypal.get_access_token(config)
    logging.debug(f"Token is: {token}")
    logging.info("Getting invoices")
    invoices = paypal.list_all_invoices([], 1, token, config)
    logging.debug(invoices)
    winner = Order(first='Joe', email=f"test_email-{randint(1,1000)}@gmail.com", item=f"Test Colorway {randint(100,10000)}", entity=f"Test Sculpt {randint(10, 1000)}", price=randint(10, 100), shipping=5)
    logging.info("Generating draft invoice")
    inv_link = paypal.generate_draft_invoice(token=token, invoice=f"TST-{randint(100,10000)}", win_data=winner, config=config)
    logging.debug(f"invLInk is: {inv_link}")
    logging.info("Getting invoice info")
    inv_number = paypal.get_invoice_info(inv_link, token, config)
    logging.debug(f"invNumber is: {inv_number}")

    return 0

if __name__ == "__main__":
    sys.exit(main())