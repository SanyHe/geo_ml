import pandas as pd
import numpy as np
from pyroxene_processor.global_variable import *
import os

def check_file(cpx_data, spl_data, pattern=1):
    """check whether the data set exists in the current directory and whether input the data set name right

    :param cpx_data: data set
    :param spl_data: data set
    :param pattern: one of three patterns
    """
    if not cpx_data == None:
        cpx_data_path = os.path.join(WORKING_PATH, cpx_data)
    else:
        raise UnboundLocalError("please input the data set name in the form of '****.xlsx'")
    if not spl_data == None:
        spl_data_path = os.path.join(WORKING_PATH, spl_data)
    if pattern == 1 or pattern == 2:
        if not os.path.isfile(cpx_data_path):
            # check the data set needed for pattern one and two exist
            raise FileNotFoundError("missing {}, please put {} in the current directory!".format(cpx_data, cpx_data))
    elif pattern == 3:
        if spl_data == None:
            raise UnboundLocalError("please input the data set name in the form of ****.xlsx")
        if not os.path.isfile(spl_data_path):
            # check the data set needed for pattern three
            raise FileNotFoundError("missing {}, please put {} in the current directory!".format(spl_data, spl_data))

def check_oxide(dataset, model=1):
    """check whether or not the oxides needed for calculating exist

    :param dataset: data for calculating cation formula
    :param model: one of the three patterns
    """
    print("Check whether the sheet contains basic oxides ......")
    data_columns = list(dataset.columns)
    if model == 1 or model == 2:
        basic_oxide = CPX_OXIDE
    elif model == 3:
        basic_oxide = SPL_OXIDE
    for i in range(len(basic_oxide)):
        if basic_oxide[i] not in data_columns:
            raise Exception("Missing Specific Oxide: ", basic_oxide[i])
    print("The data set satisfies the requirement of basic oxides")


