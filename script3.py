import pandas as pd
import sys
import time


def calc_sov_to_osv_ratio(text):
    sentences = text.split('。')
    sov_count = 0
    osv_count = 0
    for sentence in sentences:
        if not('が' in sentence and 'を' in sentence): 
            continue
        elif sentence.index('が') < sentence.index('を'):
            sov_count += 1
        elif sentence.index('が') > sentence.index('を'):
            osv_count += 1
    return sov_count, osv_count


def main(file_name, start):
    if 'xlsx' in file_name:
        df = pd.ExcelFile(file_name).parse()  # df = dataframe
        #  接続詞の 'が'　と区別するためにを除外
        df = df.drop(df[(df['品詞'] == '助詞-接続助詞') & (df['原文文字列'] == 'が')].index)
        text = ''.join(df['原文文字列'].tolist())
    else:
        reader = pd.read_csv(
            file_name,
            sep='\t',
            lineterminator='\n',
            usecols=[16, 23],  # 16=品詞行、23=原文文字列行
            chunksize=60,
            header=0,
            names=['品詞', '原文文字列']
        )
        text = ''
        sov_count = 0
        osv_count = 0
        for df in reader:
            df.to_csv('extracted.csv', mode='a', header=0)
            df.drop(df[(df['品詞'] == '助詞-接続助詞') & (df['原文文字列'] == 'が')].index)
            text += ''.join(df['原文文字列'].tolist())
            last_period_index = text.rfind('。') + 1
            if last_period_index >= 5000:  # ５千行ごとに処理する
                sov, osv = calc_sov_to_osv_ratio(text[:last_period_index])
                sov_count += sov
                osv_count += osv
                text = text[last_period_index:]
                elapsed = time.time() - start
                print(f"SOV: {sov_count}, OSV: {osv_count}, SOV to OSV Ratio: {sov_count / osv_count}")
                print(f"Time elapsed: {elapsed}")


if __name__ == "__main__":
    file_name = sys.argv[1]
    start = time.time()
    main(file_name, start)