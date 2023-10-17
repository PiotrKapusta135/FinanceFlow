import Scraper


symbols = ['AAPL', 'TSLA', 'CDR.WA', 'MSFT', '^GSCP', 'GC=F', 'CL=F']

for symbol in symbols:
    Scraper.get_recent_data(symbol)