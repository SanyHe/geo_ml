#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import os
import sys
sys.path.append("..")
from pyroxene_processor.module import *
from pyroxene_processor.global_variable import *
from pyroxene_processor.exception import *

def classify(pattern=1):
    """classify every pyroxene data into specific kind

    :param pattern: one of three patterns
    """

    cation_data = pd.read_excel(os.path.join(WORKING_PATH, 'cpx_cation_data.xlsx'), engine="openpyxl")
    result = pd.read_excel(os.path.join(WORKING_PATH, 'prediction_result.xlsx'), engine="openpyxl")

    print('Classify the pyroxene data into specific kind respectively ......')
    print("The classification results will depend on the prediction values of various ML algorithms")
    print("Classification Results:")

    if pattern == 1:
        model_name = MODEL_NAME_ONE
    elif pattern == 2:
        model_name = MODEL_NAME_TWO
    elif pattern == 3:
        model_name = MODEL_NAME_THREE

    # used for output
    output = cation_data.copy()

    # set corresponding conditions to classify the data
    J = 2 * cation_data['Na']
    for i in range(len(model_name)):
        temp = cation_data.copy()
        Fe3 = cation_data['Fe'] * result[model_name[i]]
        Fe2 = cation_data['Fe'] - Fe3
        Q = cation_data['Ca'] + cation_data['Mg'] + Fe2
        temp['condition_1'] = Q + J
        temp['condition_2'] = J / (Q + J)
        condition_3 = cation_data['Ca'] / (cation_data['Ca'] + cation_data['Mg'] + cation_data['Mn'] + Fe3 + Fe2)
        temp['condition_3'] =  condition_3
        condition_3_1 = (Fe2 + Fe3 + cation_data['Mn']) / (cation_data['Mg'] + cation_data['Mn'] + Fe2 + Fe3)
        temp['condition_3_1'] = condition_3_1
        Jd = cation_data['Na'] + cation_data['Al']
        Ae = cation_data['Na'] + Fe3
        condition_4 = Q / (Q + Jd + Ae)
        temp['condition_4'] = condition_4
        condition_4_1 = Ae / (Jd + Ae)
        temp['condition_4_1'] = condition_4_1
        # create a new column to hold the classified results
        temp['catagory'] = np.nan

        for j in range(temp.shape[0]):
            # the first condition to divide the data set into other pyroxene and the ones pending
            if temp['condition_1'].iloc[j] < 1.5:
                temp['catagory'].iloc[j] = 'Other Pyroxene'
            elif 1.5 <= temp['condition_1'].iloc[j]:
                # the second condition to further classify the pending data as Quad, Ca-Na, Na pyroxenes
                if temp['condition_2'].iloc[j] <= 0.2:
                    # the third condition to further classify the Quad pyroxene data into more small types
                    if temp['condition_3'].iloc[j] <= 0.05:
                        if temp['condition_3_1'].iloc[j] <= 0.5:
                            temp['catagory'].iloc[j] = 'Clinoenstatite'
                        elif 0.5 < temp['condition_3_1'].iloc[j]:
                            temp['catagory'].iloc[j] = 'Clinoferrosilite'
                    elif 0.05 < temp['condition_3'].iloc[j] <= 0.2:
                        temp['catagory'].iloc[j] = 'Pigeonite'
                    elif 0.2 < temp['condition_3'].iloc[j] <= 0.45:
                        temp['catagory'].iloc[j] = 'Augite'
                    elif 0.45 < temp['condition_3'].iloc[j]:
                        if temp['condition_3_1'].iloc[j] <= 0.5:
                            temp['catagory'].iloc[j] = 'Diopside'
                        elif 0.5 < temp['condition_3_1'].iloc[j]:
                            temp['catagory'].iloc[j] = 'Hedenbergite'
                elif 0.2 < temp['condition_2'].iloc[j]:
                    # the fourth condition to further classify the Ca-Na and Na pyroxene data into more small types
                    if temp['condition_4'].iloc[j] <= 0.2:
                        if temp['condition_4_1'].iloc[j] <= 0.5:
                            temp['catagory'].iloc[j] = 'Jadeite'
                        elif 0.5 < temp['condition_4_1'].iloc[j]:
                            temp['catagory'].iloc[j] = 'Aegirine'
                    elif 0.2 < temp['condition_4'].iloc[j] <= 0.8:
                        if temp['condition_4_1'].iloc[j] <= 0.5:
                            temp['catagory'].iloc[j] = 'Omphacite'
                        elif 0.5 < temp['condition_4_1'].iloc[j]:
                            temp['catagory'].iloc[j] = 'Aegirine-Augite'

        # append the classification of trained model respectively into the output sheet
        output[model_name[i]] = temp['catagory']

    print(output.iloc[:, -len(model_name):])
    # store the result in the form of '***.xlsx'
    result2sheet(output, df_name="classified_result")



