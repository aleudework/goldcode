from goldcode.utils.db_downloader import DBDownloader

table = 'lejemaal'
sql = f"select top 100 * from lejemaal"

down = DBDownloader()
down.set_default_eg_prod()

df = down.sql(sql)

print(df.head())

