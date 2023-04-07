from openpyxl import Workbook


class Writer:

    def write_excel_data(self, path, sheet_name, header, data):
        wb = Workbook()
        ws = wb.active
        ws.title = sheet_name

        row = 1 if header is None else 2
        if header is not None:
            self.__write_row_data(ws, 1, header)

        self.__write_sheet_data(ws, row, data)

        wb.save(path)
        wb.close()

    def __write_row_data(self, ws, row, rowData):
        for col, data in enumerate(rowData):
            ws.cell(row, col+1).value = data

    def __write_sheet_data(self, ws, row, data):
        for row_data in data:
            self.__write_row_data(ws, row, row_data.to_list())
            row += 1