"""Pandas Excel reader.

Pandas parser for .xlsx files.

"""
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


class PandasExcelReader(BaseReader):
    r"""Pandas-based CSV parser.

    Parses CSVs using the separator detection from Pandas `read_csv`function.
    If special parameters are required, use the `pandas_config` dict.

    Args:

        pandas_config (dict): Options for the `pandas.read_excel` function call.
            Refer to https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html
            for more information. Set to empty dict by default, this means defaults will be used.

    """

    def __init__(
        self,
        *args: Any,
        pandas_config: dict = {},
        concat_rows: bool = True,
        row_joiner: str = "\n",
        **kwargs: Any
    ) -> None:
        """Init params."""
        super().__init__(*args, **kwargs)
        self._pandas_config = pandas_config
        self._concat_rows = concat_rows
        self._row_joiner = row_joiner

    
    def load_data(
        self,
        file: Path,
        sheet_name: Optional[Union[str, int]] = None,
        extra_info: Optional[Dict] = None,
    ) -> List[Document]:
        """Parse file and extract values from a specific column.

        Args:
            file (Path): The path to the Excel file to read.
            column_name (str): The name of the column to use when creating the Document objects.
        Returns:
            List[Document]: A list of`Document objects containing the values from the specified column in the Excel file.
        """
        import pandas as pd
        import collections.abc

        df = pd.read_excel(file, sheet_name=sheet_name, **self._pandas_config)

        keys = df.keys()

        df_sheets = []
        # # add axes labels to df_sheets
        # df_sheets.append(df.axes)

        for key in keys:
            sheet = []
            for h in df[key].axes:
                sheet.append(str(h))
            sheet.append(df[key].values.astype(str).tolist())
            df_sheets.append(sheet)

        # flattens a multi-dimensional list
        def flatten(lis):
            for item in lis:
                if isinstance(item, collections.abc.Iterable) and not isinstance(item, str):
                    for x in flatten(item):
                        yield x
                else: 
                    yield item

        text_list = list(flatten(df_sheets))

        if self._concat_rows:
            return [
                Document(
                    text=self._row_joiner.join(text_list), extra_info=extra_info or {}
                )
            ]
        else:
            return [
                Document(text=text, extra_info=extra_info or {}) for text in text_list
            ]
