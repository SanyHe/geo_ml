#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pyroxene_processor.calculator_model.calculator import calculate
from pyroxene_processor.predictor_model.predictor import predict
from pyroxene_processor.classifier_model.classifier import classify
from pyroxene_processor.global_variable import *
from pyroxene_processor.exception import *

def process(cpx_data=None, spl_data=None, pattern=1):

    # check whether the data set for computation exists
    check_file(cpx_data=cpx_data, spl_data=spl_data, pattern=pattern)

    print(' ')
    pattern_dict = {1: "Pattern One",
                    2: "Pattern Two",
                    3: "Pattern Three"}
    print("*" * 15)
    print(pattern_dict[pattern])
    print("*" * 15)

    if pattern == 1 or pattern == 2:
        print("Data Loaded: \n+ {} ".format(cpx_data))
        if pattern == 1:
            model_name = MODEL_NAME_ONE
        elif pattern == 2:
            model_name = MODEL_NAME_TWO
        print("Model Prepared:")
        for i in range(len(model_name)):
            print('+ ' + model_name[i])
    elif pattern == 3:
        print("Data Loaded: \n+ {} \n+ {}".format(cpx_data, spl_data))
        print("Model Prepared:")
        for i in range(len(MODEL_NAME_THREE)):
            print('+ ' + MODEL_NAME_THREE[i])
    print("  ")
    print("*" * 15)
    print('Data Process')
    print("*" * 15)
    # load the calculator in a specific pattern to compute the corresponding cation data
    if pattern == 1 or pattern == 2:
        calculate(cpx_data, model=pattern)
    elif pattern == 3:
        calculate(cpx_data, spl_data, model=pattern)

    print("*" * 15)
    print('Model Predict')
    print("*" * 15)
    # load the trained model to predict based on the provided data
    predict(pattern=pattern)

    print("*" * 15)
    print('Classification')
    print("*" * 15)
    # classify the pyroxene data into different types
    classify(pattern=pattern)

"""
if __name__ == '__main__':
    processor(cpx_data="cpx_data.xlsx", spl_data="spl_data.xlsx", pattern=1)
"""

