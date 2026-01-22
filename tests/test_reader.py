from goldcode.utils.reader import Reader

reader = Reader()

path = '/Users/alhu/Data/Konverteringsdata/Downloadet/BilagsMapping/BilagsMapping_251231'

df = reader.load_df_from_chunks(path)

print(df.info())