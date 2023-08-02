from llama_hub.file.pandas_excel.base import PandasExcelReader
from pathlib import Path


# loads test xlsx sheet that works with and without pandas_excel fixes
def test_good_sheet():
    pandas_excel_reader = PandasExcelReader()
     
    # load the good xlsx sheet
    document = pandas_excel_reader.load_data(file=Path('tests/tests_pandas_excel/good_sheet.xlsx'))

    # check if document is loaded properly
    # note: will return error if xlsx sheet is empty
    assert len(document[0].text) > 0, "Document empty"

# loads test xlsx sheet that works only with pandas_excel fixes
# without pandas_excel fixes, reader found list instances when parsing xlsx file, not str instances
def test_bad_sheet():
    pandas_excel_reader = PandasExcelReader()
    
    # load the bad xlsx sheet
    document = pandas_excel_reader.load_data(file=Path('tests/tests_pandas_excel/bad_sheet.xlsx'))

    # check if document is loaded properly
    # note: will return error if xlsx sheet is empty
    assert len(document[0].text) > 0, "Document empty"