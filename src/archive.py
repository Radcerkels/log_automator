# coding: utf-8

import os
import shutil


def archive():
    """
    This function moves all files in the sample_logs folder to the Archives folder.
    """
    os.makedirs("Archives", exist_ok=True)

    for log in os.listdir("sample_logs"):
        shutil.move(os.path.join("sample_logs", log), "Archives")
    print("End of archive...")