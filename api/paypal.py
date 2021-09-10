import os
import sys
from datetime import datetime
import json
import logging
import requests
from requests.auth import HTTPBasicAuth


def get_access_token(config):
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en_US"
    }
    payload = {
        "grant_type": "client_credentials"
    }
    try:
        res = requests.post(
            url=f"https://{config.PAYPAL_API_URL}/v1/oauth2/token", auth=HTTPBasicAuth(config.PAYPAL_CLIENT_ID, config.PAYPAL_SECRET),  headers=headers, data=payload)
        if res.status_code == 200:
            return json.loads(res.text)["access_token"]
    except Exception as e:
        logging.error(e)
        return {}


def generate_draft_invoice(invoice, win_data, token, config):
    invoice_link = ''
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "detail": {
            "invoice_number": f"{invoice}",
            "invoice_date": datetime.now().strftime('%Y-%m-%d'),
            "currency_code": "USD",
            "note": config.INVOICE_NOTE,
            "terms_and_conditions": config.INVOICE_TANDC,
            "term": config.INVOICE_TERM,
            "memo": config.INVOICE_MEMO,
            "payment_term": {
                "term_type": "DUE_ON_RECEIPT",
                "due_date": "2021-08-12"
            },
        },
        "invoicer": {
            "email_address": config.INVOICE_EMAIL,
            "website": config.INVOICE_SITE,
            "additional_notes": config.INVOICE_ADDLNOTES
        },
        "primary_recipients": [
            {
                "billing_info": {
                    "name": {
                        "given_name": f"{win_data.first_name}",
                        "surname": f"{win_data.last_name}"
                    },
                    "email_address": f"{win_data.email}",
                }

            }
        ],
        "items": [
            {
                "name": f"{win_data.item}",
                "description": f"{win_data.entity}.",
                "quantity": "1",
                "unit_amount": {
                    "currency_code": "USD",
                    "value": f"{win_data.price}"
                },
                "unit_of_measure": "QUANTITY"
            }

        ],
        "configuration": {
            "tax_calculated_after_discount": False,
            "tax_inclusive": False,
            "allow_tip": config.INVOICE_TIP
        }
    }
    try:
        res = requests.post(
            url=f"https://{config.PAYPAL_API_URL}/v2/invoicing/invoices", headers=headers, data=json.dumps(payload))
        if res.status_code == 201:
            invoice_link = json.loads(res.text)['href']
        else:
            logging.error(
                f"Unable to complete request: {res.status_code} - {res.text}\n{payload}")
    except Exception as e:
        logging.error(e)

    return invoice_link


def generate_invoice_number(invoice, token, config):
    """Generates the next invoice number in a set

    Args:
        invoice (str): Prefix string for the invoices
        config (Config): Config object

    Returns:
        str: String with prefixed invoice set and latest invoice number
    """
    invoice_number = ""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    try:
        res = requests.post(
            url=f"https://{config.PAYPAL_API_URL}/v2/invoicing/generate-next-invoice-number", headers=headers)
        if res.status_code == 200:
            invoice_number = res.text
        elif res.status_code == 401:
            token = get_access_token(config)
            invoice_number = generate_invoice_number(invoice, token, config)
        else:
            logging.error(
                f"Unable to complete request: {res.status_code} - {res.reason}")

    except:
        pass
    return invoice_number


def list_all_invoices(invoices, page, token, config):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "page": page,
        "page_size": 10,
        "total_required": "true"
    }
    logging.debug(headers, payload)
    try:
        res = requests.get(
            url=f"https://{config.PAYPAL_API_URL}/v2/invoicing/invoices", headers=headers, params=payload)
        logging.debug(res.status_code)
        if res.status_code == 200:
            data = json.loads(res.text)
            if data['total_items'] > 0:
                for invoice in data['items']:
                    invoices.append(invoice)
                if page < data['total_pages']:
                    invoices = list_all_invoices(
                        invoices, page+1, token, config)
        elif res.status_code == 401:
            token = get_access_token(config)
            list_all_invoices(invoices, page, token, config)

        else:
            logging.error(
                f"Unable to complete request: {res.status_code} - {res.reason}")
    except Exception as e:
        logging.error(e)

    return invoices

def get_invoice_info(link, token, config):
    inv_number = ''
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    try:
        res = requests.get(url=link, headers=headers)
        if res.status_code == 200:
            data = json.loads(res.text)
            inv_number = data['detail']['invoice_number']
        elif res.status_code == 401:
            inv_number = get_invoice_info(link, token, config)
        else:
            logging.error(
                f"Unable to complete request: {res.status_code} - {res.text}")
    except Exception as e:
        pass
    return inv_number

def main():
    pass


if __name__ == '__main__':
    sys.exit(main())
