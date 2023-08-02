# This is for restarting of the computer based on Excel
import openpyxl
import time
import os

threshold = 5


def restart():
    time.sleep(60)
    os.system("shutdown /r /t 0")


def check_file():
    workbook = openpyxl.load_workbook('restart_times.xlsx')
    sheet = workbook.active
    counter = sheet["B1"].value
    # 到迴圈上限
    if counter == threshold:
        print("done")
    # 還沒:去更新
    else:
        # 更新log資訊
        sheet["B1"] = counter + 1
        workbook.save('restart_times.xlsx')
        restart()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    check_file()
