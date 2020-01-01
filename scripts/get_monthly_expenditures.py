#!/usr/local/bin/python3

# PURPOSE =========================================================================================
# Create a CSV file containing a summary of monthly Tangerine credit card expenses.
#
# USE =============================================================================================
# 'python3 get_monthly_expenditures.py [ csv file ]'.
#
###################################################################################################

# TODO: yearly summary
# TODO: datastore
# TODO: cron
# TODO: scrape
# TODO: track credits
# TODO: monthly totals
# TODO: generalize for other banks

import subprocess
import os
import argparse
import sys
import requests
import time
import datetime as dt
import pandas as pd
import re
from datetime import datetime

def main() :
    file = sys.argv[1]
    if len(file) > 0 :
        df = prepare_dataframe(file)
        df = df.groupby('transaction_category').sum()
        df = df.drop(['Amount', 'rewards_earned'], axis=1)
        df.reset_index().to_csv(os.path.splitext(file)[0] + '_summary.csv')
    else : 
        sys.exit("Provide monthly transactions to be summarized.")

def prepare_dataframe(monthly_expenses_csv) :
    df = pd.read_csv(monthly_expenses_csv, encoding = 'ISO-8859-1')
    if not df.empty :
        df['transaction_category'] = df.apply(lambda row: get_transaction_category(row['Memo'], 'Category: '), axis=1)
        df['rewards_earned'] = df.apply(lambda row: get_rewards_earned(row['Memo']), axis=1)
        df['Amount'] = df.apply(lambda row: remove_credits(row['Amount']), axis=1)
        df['transaction_amount'] = df['Amount'] + df['rewards_earned']
    return df

def get_transaction_category(memo, delimiter) :
    if isinstance(memo, unicode) :
        return memo[memo.index(delimiter) + len(delimiter):]
    else :
        return 'None'

def get_rewards_earned(memo) :
    if isinstance(memo, str) :
        match = re.search(r'(?s)(?<=Rewards earned: ).*?(?= ~ Category:)', memo)
        return float(match.group(0))
    else :
        return 0

def remove_credits(amount) :
    return 0 if amount > 0 else amount

main()