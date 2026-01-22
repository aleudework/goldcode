from goldcode.utils.dataframeloader import DataFrameLoader

reader = DataFrameLoader()

path = '/Users/alhu/Data/Konverteringsdata/Downloadet/BilagsMapping/BilagsMapping_251231'

df = reader.load_df_from_chunks(path)

print(df.info())