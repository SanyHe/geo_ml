#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#from module import result2sheet, model_relaunch
import sys
sys.path.append("..")
from pyroxene_processor.module import *
from pyroxene_processor.global_variable import *
import os
import pandas as pd

def base_predictor(data, pattern=1):
    """choose specific pattern to relaunch the trained model for user's data set

    :param data: user's data set for predicting
    :param pattern: options for three patterns
    """
    if pattern == 1:
        model_name = MODEL_NAME_ONE
        model = MODEL_ONE
    elif pattern == 2:
        model_name = MODEL_NAME_TWO
        model = MODEL_TWO
    elif pattern == 3:
        model_name = MODEL_NAME_THREE
        model = MODEL_THREE

    result = model_relaunch(pattern, model_name, model, data)
    result2sheet(result, df_name="prediction_result")

def predict(pattern=1):
    """relaunch trained model in a specific pattern

    :param pattern: one of the three pattern
    """
    if pattern == 1 or pattern == 2:
        # load cpx data for pattern one and pattern two
        cpx_data_path = os.path.join(WORKING_PATH, 'cpx_cation_data.xlsx')
        data = pd.read_excel(cpx_data_path, engine="openpyxl")
        base_predictor(data, pattern)
    if pattern == 3:
        # load cpx data and spl data for pattern three
        cpx_data_path = os.path.join(WORKING_PATH, 'cpx_cation_data.xlsx')
        cpx_data = pd.read_excel(cpx_data_path, engine="openpyxl")
        spl_data_path = os.path.join(WORKING_PATH, 'spl_cation_data.xlsx')
        spl_data = pd.read_excel(spl_data_path, engine="openpyxl")
        # merge two sheets of cpx and spl cation data into one sheet along columns
        data_combined = pd.concat([cpx_data, spl_data], axis=1)
        base_predictor(data_combined,pattern)

