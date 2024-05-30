import pandas as pd

def download_nfl_data(years, cols_of_interest):
    data = pd.DataFrame()
    for YEAR in years:  
        i_data = pd.read_csv('https://github.com/nflverse/nflverse-data/releases/download/pbp/' \
                    'play_by_play_' + str(YEAR) + '.csv.gz',
                    compression= 'gzip', low_memory= False)
        # data = data.append(i_data, sort=True)
        data = pd.concat(objs=[data, i_data])
        data = data[cols_of_interest]
        return data
