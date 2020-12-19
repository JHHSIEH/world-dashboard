# https://github.com/M-Media-Group/Covid-19-API
# https://restcountries.eu/
# https://datahelpdesk.worldbank.org/knowledgebase/topics/125589-developer-information

# explore available world bank statistics with these URIs:
# https://api.worldbank.org/v2/sources?format=json
# https://api.worldbank.org/v2/sources/15/indicators?format=json

from datetime import datetime
from http_request import request

COVID_BASE_URL = 'https://covid-api.mmediagroup.fr/v1'
COUNTRIES_BASE_URL = 'https://restcountries.eu/rest/v2'
WORLDBANK_BASE_URL = 'https://api.worldbank.org/v2'

VALID_COVID_STATUSES = ['Confirmed', 'Deaths', 'Recovered']
VALID_COUNTRY_REGIONS = ['Africa', 'Americas', 'Asia', 'Europe', 'Oceania']
SUPPORTED_WORLDBANK_INDICATORS = [
    'UNEMPSA_', # Unemployment rate,Percent,,,
    'CORESA', # Core CPI,seas.adj,,,
    'CPTOTSAXMZGY', # CPI Price, % y-o-y, median weighted, seas. adj.
    'DSTKMKTXD', # Stock Markets, US$
    'DSTKMKTXN', # Stock Markets, LCU
    'EN.ATM.CO2E.KT', # CO2 emissions (kt)
    'EN.ATM.CO2E.PC', # CO2 emissions (metric tons per capita)
    'EN.ATM.CO2E.PP.GD', # CO2 emissions (kg per PPP $ of GDP)
    'EN.POP.SLUM.UR.ZS', # Population living in slums (% of urban population)
    'HD.HCI.OVRL,' # Human Capital Index (HCI) (scale 0-1)
    'SH.DTH.COMM.ZS', # Cause of death, by communicable diseases and maternal, prenatal and nutrition conditions (% of total)
    'SI.DST.FRST.10', # Income share held by lowest 10%
    'SI.DST.FRST.20', # Income share held by lowest 20%
    'SI.DST.02ND.20', # Income share held by second 20%
    'SI.DST.03RD.20', # Income share held by third 20%
    'SI.DST.04TH.20', # Income share held by fourth 20%
    'SI.DST.05TH.20', # Income share held by highest 20%
    'SI.DST.10TH.10', # Income share held by highest 10%
    'SI.POV.NAHC', # Poverty headcount ratio at national poverty lines (% of population)
    'SI.POV.LMIC', # Poverty headcount ratio at $3.20 a day (2011 PPP) (% of population)
    'FP.CPI.TOTL', # Consumer price index (2010 = 100)
    'FP.CPI.TOTL.ZG', # Inflation, consumer prices (annual %)
]

def validate_case_insensitive_string_input(valid_inputs, input_to_validate):
    valid_inputs = [item.lower() for item in valid_inputs]
    if input_to_validate.lower() not in valid_inputs: 
        raise ValueError((
            f'invalid input: {input_to_validate}; ' +
            f'input must be one of {valid_inputs}'))

def get_covid_cases_by_country_abbrev(country='ca'):
    url = COVID_BASE_URL + f'/cases?ab={country}'
    result = request(url)
    return result

def get_covid_history_by_country_abbrev_and_status(
        country='ca', status='confirmed'):
  
    validate_case_insensitive_string_input(VALID_COVID_STATUSES, status)
    
    url = COVID_BASE_URL + f'/history?ab={country}&status={status}'
    result = request(url)
    return result

def get_countries_search_by_name(search_term='united'):
    url = COUNTRIES_BASE_URL + f'/name/{search_term}'
    result = request(url)
    return result

def get_countries_search_by_region(region='americas'):
    validate_case_insensitive_string_input(VALID_COUNTRY_REGIONS, region)

    url = COUNTRIES_BASE_URL + f'/region/{region}'
    result = request(url)
    return result

def dt_str_to_yr_mt(date_str):
    return datetime.strftime(datetime.strptime(date_str, '%Y-%m-%d'), '%YM%m')

def get_worldbank_stat(
        indicator='UNEMPSA_', 
        country='ca', 
        daterange_list=['2020-01-01','2020-12-31']):

    validate_case_insensitive_string_input(
        SUPPORTED_WORLDBANK_INDICATORS, 
        indicator)

    url = (
        WORLDBANK_BASE_URL + f'/country/{country}/indicator/{indicator}' +
        f'?date={dt_str_to_yr_mt(daterange_list[0])}:' + 
        f'{dt_str_to_yr_mt(daterange_list[1])}&format=json&page=1')
    result = request(url)
    return result

if __name__ == '__main__':
    res = get_covid_history_by_country_abbrev_and_status(status='asdf')
    print(res)