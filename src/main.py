#coding=utf-8
from parse_logs import *
from send_mail import *
from generate_report import *
from archive import *
import pandas as pd
from send_mail import *



def __main__():



    """
    We will list all .log files in sample_logs/ then apply the parse_logs_files() function
    on each of them and save organized .log in logs/ and .csv reports of each of them in reports/
    """
    reports = {}
    log_dir = os.listdir("sample_logs")
    if not log_dir:
        return print("Nothing logs in sample_logs/ Goodbye...")
    
    for log in log_dir:
        result = parse_log_file(os.path.join("sample_logs", log))
    
        reports = merge(result, reports)

    """
    repports = {key : report_name, value : dict}
    So we will convert each value with pandas and create .csv reports
    """
    for key , value in reports.items():
        df = pd.DataFrame(value)
        df.to_csv(os.path.join(os.getcwd(),"reports", key.replace(".log",".csv")), index = False)
    print("End of .log file's organisation...")

    """
    We save the .log of sample_logs/ in Archives/ after traitment
    """
    archive()


    


if __name__ == "__main__":
    __main__()