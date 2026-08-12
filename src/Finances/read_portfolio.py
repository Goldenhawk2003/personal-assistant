import pathlib
import pandas as pd
import numpy as np
import csv
import datetime as dt
from sqlalchemy import create_engine


class PortfolioReader:
    def __init__(self):
        self.directory = pathlib.Path(
            "C:\\Users\\ammar\\OneDrive\\Documents\\TFSA_Portfolios"
        )
        self.engine = create_engine(
            "mysql+pymysql://root:Ammar2003@127.0.0.1:3306/portfolio"
        )

    def save_to_db(self, data: pd.DataFrame):
           data.to_sql(
        name="portfolio_history",
        con=self.engine,
        if_exists="append",
        index=False,
    )
           data.to_sql(
               name="latest_portfolio",
               con=self.engine,
                if_exists="replace",
                index=False,
           )

    def read_portfolio(self):
        files = list(self.directory.glob("holdings-report-*.csv"))

        if not files:
            raise FileNotFoundError(
                f"No holdings reports found in {self.directory}"
            )

        latest_file = max(
            files,
            key=lambda file: file.stat().st_mtime
        )
 

        try:
            columns = [
            "Symbol",
            "Market Price Currency",
            "Quantity",
            "Market Price",
            "Book Value (CAD)",
            "MIC",
            ]

            data = pd.read_csv(
                latest_file,
                usecols=columns,)
            data = data.rename(
                columns={
                    "Symbol": "Ticker",
                    "MIC": "MIC",
                    "Quantity": "Shares",
                    "Market Price": "Quote",
                    "Market Price Currency": "Currency",
                    "Book Value (CAD)": "Book Value",
                }
            )

            
            report_date = dt.datetime.strptime(
                latest_file.stem.replace("holdings-report-", ""),
                "%Y-%m-%d"
            ).date()
            
            data["Date"] = report_date
            self.save_to_db(data)
            return data

        except Exception as e:
            raise ValueError(
                f"An error occurred while reading {latest_file}: {e}"
            ) from e