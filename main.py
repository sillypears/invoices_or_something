import os, sys
import argparse
import logging
from configs.config import app_config

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--env', dest='env', required=True, help='Set environment')
    parser.add_argument('-f', '--file', dest='input_file', help='Input file with winners to invoice')
    parser.add_argument('-s', '--set', dest='set', help='Project set for invoice IDs')
    args = parser.parse_args()
    config = app_config[args.env]
    if not os.path.exists('logs'):
        os.mkdir('logs')
    logging.basicConfig(filename='logs/main.log', encoding='utf-8', level=logging.DEBUG if config.DEBUG else logging.INFO)
    
if __name__ == "__main__":
    sys.exit(main())