#! /usr/bin/python3
# weather.py - Scrape weather history from www.wunderground.com
# Only four attributes are returned, which are average temperature, average
# humidity, precipitation, and date.
# This script is better imported to jupyter notebook and do data visulization
# and manipulation there because of better pandas integration.


import requests
import bs4
import pandas as pd


def main():
    start_date = '2015/01/01'
    end_date = '2015/12/31'
    airport = 'SBGR'
    header()
    html = get_html_from_web(airport=airport, start_date=start_date,
                             end_date=end_date)
    table = get_data_from_html(html)
    df_empty = build_dataframe(table)
    df_populated = populate_dataframe(df_empty, table)
    df_final = cleanup_dataframe(df_populated, start_date=start_date,
                                 end_date=end_date)

    df_final.to_csv('weather.csv')


def header():
    print()
    print('-------------------------------')
    print('        Weather App')
    print('-------------------------------')
    print()


def get_html_from_web(airport='SBGR', start_date='2015/01/01',
                      end_date='2015/12/31'):
    """
    Get html script that contains all the weather data.

    Parameters
    ----------
    airport: str
        Four capital letters representing ICAO code for an airport.
    start_date: str
        Follow the format of YYYY/MM/DD (2015/01/31)
    end_date: str
        Follow the format of YYYY/MM/DD (2015/11/30)

    Returns
    -------
    Raw html script of the whole website.
    """

    url = 'https://www.wunderground.com/history/airport/{}/{}/CustomHistory.html\
        ?dayend={}&monthend={}&yearend={}'.format(
        airport, start_date, end_date[8:], end_date[5:7], end_date[0:4]
    )
    response = requests.get(url)

    return response.text


def get_data_from_html(html):
    """
    Parse html and get a table that contains all the weather info.

    Parameters
    ----------
    html: str
        text from request

    Return
    ------
    BeautifulSoup tag object.
    """
    soup = bs4.BeautifulSoup(html, 'html.parser')
    table = soup.find(id='obsTable')

    return table


def build_dataframe(tag):
    """
    Build an empty dataframe with the correct column names and indices.

    Parameter
    ---------
    tag: obj
        BeautifulSoup tag.

    Return
    ------
    Pandas DataFrame obj.
    """

    n_rows = 0
    n_columns = len(tag.find_all('tr')[1].find_all('td'))
    for row in tag.find_all('tr'):
        if row.a:
            n_rows += 1

    return pd.DataFrame(columns=range(n_columns), index=range(n_rows))


def populate_dataframe(df, tag):
    """
    Populate the empty dataframe with the data from the website.

    Parameter
    ---------
    df: obj
        Pandas DataFrame obj.
    tag: obj
        BeautifulSoup tag.

    Return
    ------
    Pandas DataFrame obj.
    """

    row_maker = 0
    for row in tag.find_all('tr'):
        if row.a:
            column_maker = 0
            columns = row.find_all('td')
            for column in columns:
                df.iloc[row_maker, column_maker] = column.get_text().strip()
                column_maker += 1
            if len(columns) > 0:
                row_maker += 1

    return df


def cleanup_dataframe(df, start_date='2015/01/01', end_date='2015/12/31'):
    """
    Polish and add date column to the dataframe.

    Parameter
    ---------
    df: obj
        Pandas DataFrame obj.
    start_date: str
        date in the format of YYYY/MM/DD.
    end_date: str
        date in the format of YYYY/MM/DD.

    Return
    ------
    Pandas DataFrame obj.
    """

    df = df[[2, 8, 19]]
    column_names = ['Average_Temperature', 'Average_Humidity', 'Precipitation']
    df.columns = column_names
    date = pd.date_range(start=start_date, end=end_date)
    df.loc[:, 'date'] = date
    df[column_names] = df[column_names].apply(
        pd.to_numeric, axis=1, errors='coerce')

    return df


if __name__ == '__main__':
    main()
