import yfinance as yf
from yfinance import ticker

tickers = yf.Tickers('MSFT AAPL GOOG')
tickers.tickers['MSFT'].info
yf.download(['MSFT', 'AAPL', 'GOOG'], period='1mo')

spy = yf.Ticker('SPY').funds_data
spy.description
spy.top_holdings



class MarketData:

    def __init__(self, ticker) -> None:
        self.ticker = ticker
        self.data = yf.Ticker(ticker)   

    def get_stock_data(self, ticker, data_type):
        stock = yf.Ticker(ticker)
        if data_type == "info":
            return stock.info
        elif data_type == "calendar":
            return stock.calendar
        elif data_type == "analyst_price_targets":
            return stock.analyst_price_targets
        elif data_type == "quarterly_income_stmt":
            return stock.quarterly_income_stmt
        elif data_type == "history":
            return stock.history
        elif data_type == "option_chain":
            return stock.option_chain

    def get_sector_data(self, sector):
        sector_data = yf.Sector(sector)
        return {
            "key": sector_data.key,
            "name": sector_data.name,
            "symbol": sector_data.symbol,
            "ticker": sector_data.ticker,
            "overview": sector_data.overview,
            "top_companies": sector_data.top_companies,
            "research_reports": sector_data.research_reports
        }
    