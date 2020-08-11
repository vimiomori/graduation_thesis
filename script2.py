import pandas as pd
import numpy as np
import sys
import time

from pandas import Index

def calc_sov_to_osv_ratio(df):
    print(df.head())
    print(df.tail())

    sov_count = 0
    osv_count = 0

    period_index = find_period(df, last=False)
    while period_index:
        sentence = df[:period_index+1]
        comma = find_period(sentence, last=False, val='、')
        if comma:
            phrases = [sentence[:comma+1], sentence[comma+1:]]
        else:
            phrases = [sentence]
        count_sov_osv(phrases)
        df = df[period_index+1:]
        period_index = find_period(df, last=False)
    return sov_count, osv_count


def count_sov_osv(phrases):
    print([phrase for phrase in phrases])


def find_period(df, last=True, val='。'):
    try:
        arr = Index(df['原文文字列']).get_loc(val)
        res = np.where(arr == True)
        print(res)
        if last:
            return res[0][-1]
        else:
            return res[0][0]
    except KeyError:
        return False



def main(start):
    reader = pd.read_csv(
        'extracted.csv',
        chunksize=60,
    )
    sov_count = 0
    osv_count = 0
    for_processing = pd.DataFrame(columns=['品詞', '原文文字列'])
    rows = 0
    for df in reader:
        for_processing = for_processing.append(df) 
        rows += 60
        if rows >= 5000:  # ５千行ごとに処理する
            last_period_index = find_period(for_processing) + 1
            calc_sov_to_osv_ratio(for_processing[:last_period_index])
            # sov_count += sov
            # osv_count += osv
            for_processing = for_processing[last_period_index:]
            for_processing.columns = ['品詞', '原文文字列']
            rows = for_processing.shape[0]
            # elapsed = time.time() - start
            # print(f"SOV: {sov_count}, OSV: {osv_count}, SOV to OSV Ratio: {sov_count / osv_count}")
            # print(f"Time elapsed: {elapsed}")


if __name__ == "__main__":
    start = time.time()
    main(start)