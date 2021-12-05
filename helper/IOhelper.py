import csv

def write_to_file(item):
    file_name = "tempfile/PLS.csv"
    # "a"为追加模式（添加）
    # utf_8_sig格式导出csv不乱码
    with open(file_name, "a", encoding="utf_8_sig", newline="") as f:
        fieldnames = ["期号", "中奖号码", "开奖日期"]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writerow(item)