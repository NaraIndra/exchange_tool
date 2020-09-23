from data_processing.db_processing import update_currency

def test_update_currency():
    new_currency = update_currency()
    assert new_currency == True