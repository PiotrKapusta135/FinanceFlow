import pandas as pd
import mplfinance as fplt
from fpdf import FPDF
import matplotlib.pyplot as plt

from sqlalchemy import create_engine

import config_file

user = config_file.user
password = config_file.password
db = config_file.db
host = config_file.host
port = config_file.port

url = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(user, 
                                                password,
                                                host,
                                                port,
                                                db)

engine = create_engine(url)
query = 'select * from "Trading"."Stocks" where "Symbol" in (\'AAPL\', \'TSLA\')'

df = pd.read_sql(query, engine)
tsla_df = df.loc[df['Symbol']=='TSLA']
tsla_df = tsla_df.set_index('Date')

tsla_df.index = pd.to_datetime(tsla_df.index)


plot = fplt.plot(tsla_df,
          type='candle',
          style='charles',
          volume=True,
          savefig=dict(fname='tsla_candle.png', dpi=100, pad_inches=0.25))

pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 12)
pdf.cell(40, 10, 'Daily TSLA Data')
pdf.ln(20)
pdf.image('/home/piotrek/Projects/FinanceFlow/tsla_candle.png', w=170, h=100)
pdf.ln(20)
pdf.output('TSLA_report.pdf', 'F')
