from mylescgthomaspy.data import download_nfl_data

def test_1():
    assert 1 == 1

def test_2():
    assert 2 == 2

def test_nfl_data_exists():
    df = download_nfl_data(range(2018, 2020 + 1), ["posteam", "wp", "play_type"])
    num_rows = df.shape[0]
    assert num_rows > 0
