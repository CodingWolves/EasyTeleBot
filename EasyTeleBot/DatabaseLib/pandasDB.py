from os.path import isfile

from pandas import read_csv, DataFrame


class DB:
    def __init__(self, csv_path: str):
        self.data: DataFrame
        self.csv_path = csv_path
        if isfile(self.csv_path):
            self.data = read_csv(csv_path, memory_map=True)
        else:
            open(self.csv_path, 'x')
            print("created new file at path - '{}'".format(self.csv_path))
            self.data = read_csv(csv_path, memory_map=True)

    def AddRow(self, item, important_column=None):
        if important_column:
            ds = self.GetRowByColumnValue(important_column, item[important_column])
            if ds is not None and not ds.empty:
                self.UpdateRow(item, ds.name)
                return

        if issubclass(type(item), dict):
            self.data = self.data.append(DataFrame(data=item, index=[self.GetUnusedIndex()]),
                                         ignore_index=not important_column)
        elif issubclass(type(item), DataFrame):
            self.data = self.data.append(item, ignore_index=not important_column)
        else:
            raise Exception('uncaught item type {}'.format(type(item)))

    def UpdateRow(self, item: dict, index: int):
        indexes_list = [index for _ in range(1)]
        self.data.update(DataFrame(data=item, index=indexes_list), overwrite=True)

    def UpdateRowByColumnValue(self, updated_row: dict, column_name: str, column_value):
        for row in self.data.iloc:
            if row[column_name] == column_value:
                self.data.update(DataFrame(data=updated_row, index=[row.name]), overwrite=True)

    def GetRowByColumnValue(self, column_name: str, column_value):
        frame_result = self.data.loc[self.data[column_name] == column_value]
        if frame_result.empty:
            return None
        row_result = frame_result.iloc[0]
        return row_result

    def GetUnusedIndex(self):
        if self.data.empty:
            return 0
        return self.data.index.values.max()

    def SaveRow(self, row: int):
        self.data.to_csv(self.csv_path, index=False)

    def __save__(self):
        self.data.to_csv(self.csv_path, index=False)

    def __load__(self):
        self.data = read_csv(self.csv_path, memory_map=True)

    @classmethod
    def GetChatOnlyRow(cls, csv_path, chat):
        row = 0
        if chat.db_row is not None:
            row = chat.db_row
        csv = read_csv(csv_path, skiprows=range(1, row + 1, 1), nrows=1, memory_map=True)
        if type(csv) is DataFrame:
            for row in csv.iloc:
                if row['id'] == chat.id:
                    return row
        return None
