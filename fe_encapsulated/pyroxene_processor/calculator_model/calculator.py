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

def base_calculator(dataset, model=1):
    data_path = os.path.join(WORKING_PATH, dataset)
    try:
        data = pd.read_excel(data_path, engine='openpyxl')
    except ModuleNotFoundError:
        print("** Please download openpyxl by pip3 **")

    # replace the data whose kind is string with specific number 'NULL2VALUE'
    data = check_data_type(data)

    # fill the missing value with specific number 'NULL2VALUE'
    data = missing_filled(data, NULL2VALUE)
    # print(data.head())

    # combine the columns of FeO and Fe2O3 in a specific formula
    data = merge_fe(data)
    print("The oxides sheet: ")
    print(data)

    # check whether the basic oxides data is included in the data set
    check_oxide(data, model)

    print("Calculate cation data ......")

    # the name of the oxides
    data_columns = list(data.columns)

    # the number of cation and oxygen atom
    ion_num, oxy_num = find_num(data_columns)

    # the name of the cation
    ion = find_cation(data_columns)

    # relative molecular mass
    rmw = rel_mole_weight(ion, ion_num, oxy_num)

    # calculate the normalization factor
    normalization_factor = normalization_factor_calculation(rmw, oxy_num, data, model)

    # calculate the cation of the formula
    cation_formula = cation_formula_calculation(normalization_factor, rmw, ion_num, data, ion)

    # extract the designated columns according to different models
    if model == 1 or model == 2:
        cation_df = cation_formula[CPX_ION]
    elif model == 3:
        cation_df = cation_formula[SPL_ION]

    # change the value which is zero into 0.0000001
    cation_df_transformed = transform(cation_df)
    print("Replace the cation data 0 with 0.0000001")
    print("The cation sheet :")
    print(cation_df_transformed)

    # store the data in the form of .xlsx file
    result2sheet(cation_df_transformed, model=model)

def calculate(cpx_dataset, spl_dataset=None, model=1):
    if model == 1 or model == 2:
        print("Processing the cpx data sheet ......")
        base_calculator(cpx_dataset, model)
    elif model == 3:
        print("Processing the cpx data sheet ......")
        base_calculator(cpx_dataset, 1)
        print("Processing the spl data sheet ......")
        base_calculator(spl_dataset, 3)



