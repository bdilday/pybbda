
from pybaseballdatana.data.tools import LahmanData

def test_lahman_datadum():
    lahman_data = LahmanData()
    assert len(lahman_data.batting) == 105861
    
