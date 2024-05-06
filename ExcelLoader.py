import pandas
import pathlib
from pandas import DataFrame
from pathlib import Path


class ExcelLoader():

    def __init__(self) -> None:
        """ constructor """

        self.excel_file_list: list[Path] = []
        self.load_success: bool = False
        return

    def load(self, dir_path: str) -> None:
        """ load excel files (just loading file names)

        Args:
            dir_path (str): root directory of excel files
        """

        self.excel_file_list = [f for f in pathlib.Path(dir_path).glob("*.xlsx")]
        if len(self.excel_file_list):
            self.load_success = True

    def get_file_num(self) -> int | None:
        if self.load_success is False:
            return None

        return len(self.excel_file_list)

    def get_data_frame(self, id: int) -> DataFrame | None:
        """ get data frame of the id

        Args:
            id (int): id of dataframe (0 to the end of self.excel_file_list)

        Returns:
            DataFrame: data frame of the id
        """

        if self.load_success is False:
            return None

        data_frame = pandas.read_excel(self.excel_file_list[id])

        return data_frame
