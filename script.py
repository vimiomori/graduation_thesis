import pandas as pd
import sys
import time


def calc_sov_to_osv_ratio(text):
    sentences = text.split('。')
    sov_count = 0
    osv_count = 0
    for sentence in sentences:
        if ('が' in sentence and 'を' in sentence):
            if sentence.index('が') < sentence.index('を'):
                sov_count += 1
            elif sentence.index('が') > sentence.index('を'):
                osv_count += 1
        elif ('が' in sentence and 'に' in sentence):
            if sentence.index('が') < sentence.index('に'):
                sov_count += 1
            elif sentence.index('が') > sentence.index('に'):
                osv_count += 1
        elif ('が' in sentence and 'へ' in sentence):
            if sentence.index('が') < sentence.index('へ'):
                sov_count += 1
            elif sentence.index('が') > sentence.index('へ'):
                osv_count += 1
        elif ('は' in sentence and 'を' in sentence):
            if sentence.index('は') < sentence.index('を'):
                sov_count += 1
            elif sentence.index('は') > sentence.index('を'):
                osv_count += 1
        elif ('は' in sentence and 'に' in sentence):
            if sentence.index('は') < sentence.index('に'):
                sov_count += 1
            elif sentence.index('は') > sentence.index('に'):
                osv_count += 1
        elif ('は' in sentence and 'へ' in sentence):
            if sentence.index('は') < sentence.index('へ'):
                sov_count += 1
            elif sentence.index('は') > sentence.index('へ'):
                osv_count += 1
        else:
            continue

        # if not any([
        #     ('は' in sentence and 'を' in sentence),
        #     ('は' in sentence and 'に' in sentence),
        #     ('は' in sentence and 'へ' in sentence)
        # ]): 
        #     continue
        # elif any([
        #     sentence.index('が') < sentence.index('に'),
        #     sentence.index('が') < sentence.index('へ'),
        #     sentence.index('は') < sentence.index('を'),
        #     sentence.index('は') < sentence.index('に'),
        #     sentence.index('は') < sentence.index('へ')
        # ]):
        #     sov_count += 1
        # elif any([
        #     sentence.index('が') > sentence.index('に'),
        #     sentence.index('が') > sentence.index('へ'),
        #     sentence.index('は') > sentence.index('を'),
        #     sentence.index('は') > sentence.index('に'),
        #     sentence.index('は') > sentence.index('へ')
        # ]):
        #     osv_count += 1
    return sov_count, osv_count


def main(start):
    reader = pd.read_csv(
        'extracted.csv',
        chunksize=60,
    )
    text = ''
    sov_count = 0
    osv_count = 0
    for df in reader:
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
    start = time.time()
    main(start)