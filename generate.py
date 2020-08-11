import pandas as pd
import sys
from openpyxl import load_workbook

def kakimaze(df):
    cols = list('OをSがV')
    df = df[cols]
    return df

def drop_joshi(df):
    df = df.drop(['が', 'を'], axis=1)
    return df

def main(file_name):
    sheet_names = ['意味なし文', '意味あり文', '行為者ー対象']
    df_dict = pd.read_excel(file_name, sheet_name=sheet_names)
    book = load_workbook(file_name)
    writer = pd.ExcelWriter(file_name, engine = 'openpyxl')
    writer.book = book
    for sheet_name, df in df_dict.items(): 
        osv_joshi = kakimaze(df)
        sov_no_joshi = drop_joshi(df)
        osv_no_joshi = drop_joshi(osv_joshi)
        osv_joshi.to_excel(writer, sheet_name=f'{sheet_name}_OSV_助詞あり', index=False)
        sov_no_joshi.to_excel(writer, sheet_name=f'{sheet_name}_SOV_助詞なし', index=False)
        osv_no_joshi.to_excel(writer, sheet_name=f'{sheet_name}_OSV_助詞なし', index=False)
    writer.save()
    writer.close()

if __name__ == "__main__":
    file_name = sys.argv[1]
    main(file_name)