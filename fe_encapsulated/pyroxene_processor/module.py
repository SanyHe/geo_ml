#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyroxene_processor.global_variable import *
import pandas as pd
import numpy as np
import joblib
import os
import re
from sklearn.preprocessing import PolynomialFeatures

import warnings

# suppress the warning caused by sklearn
warnings.filterwarnings('ignore')

def str2value(single_data):
    """replace string value like 'NaN' with a int value

    :param single_data: sting value
    :return: int value
    """
    if type(single_data) == str:
        single_data = NULL2VALUE
    return single_data

def check_data_type(dataset):
    """transform all the string data into int value

    :param dataset: data set
    :return: data set with all int value
    """
    data_transform = dataset.applymap(str2value)
    return data_transform

def missing_filled(dataset, filled_number=0):
    """fill the missing values with specific number, the default number is 0

    :param dataset: data set
    :param filled_number: the number replaces null value
    :return:
    """
    dataset.fillna(filled_number, inplace=True)
    print("The missing value will be filled with default value 0")
    return dataset

def merge_fe(dataset):
    """combine the columns of Fe2O3 and FeO in the formula of 0.8998 * Fe2O3 + FeO

    :param dataset: data set
    :return: data set with the transformation of FeO
    """
    print("Combine the columns of 'Fe2O3' and 'FeO' in the formula of (0.8998 * Fe2O3 + FeO)")
    print("Remove the columns of 'FeO' and 'Fe2O3' from the oxides sheet")
    print("Append a new column named 'FeO' with the computation results")
    new_dimension = 0.8998 * dataset["Fe2O3"] + dataset["FeO"]
    dataset_drop = dataset.drop(['Fe2O3', 'FeO'], axis=1)
    dataset_drop['FeO'] = new_dimension
    return dataset_drop

def find_num(formula):
    """find the number of cation and oxygen atom in the formula

    :param formula: the molecular formula
    :return: the number of cation and oxygen atom
    """
    length = len(formula)
    temp_cation_num = [re.findall('\d?O', formula[i], re.I) for i in range(length)]
    cation_num = []
    for i in range(length):
        cation_num.extend(temp_cation_num[i])
    for j in range(length):
        cation_num[j] = re.findall('\d*', cation_num[j])[0]
        if cation_num[j] == '':
            cation_num[j] = 1
        else:
            cation_num[j] = int(cation_num[j])

    temp_oxy_num = [re.findall('O\d?', formula[i], re.I) for i in range(length)]
    oxy_num = []
    for i in range(length):
        oxy_num.extend(temp_oxy_num[i])
    for j in range(length):
        oxy_num[j] = re.findall('\d*', oxy_num[j])[1]
        if oxy_num[j] == '':
            oxy_num[j] = 1
        else:
            oxy_num[j] = int(oxy_num[j])
    return cation_num, oxy_num

def find_cation(formula):
    """find the cation of the formula

    :param formula: the molecular formula
    :return: cation
    """
    length = len(formula)
    temp = []
    for i in range(length):
        a = re.findall('[a-zA-Z]{1,2}[\d*]?', formula[i], re.I)
        temp.append(a[0])
    cation = []
    for i in range(length):
        cation.extend(re.findall('[a-zA-Z]{1,2}', temp[i], re.I))
    return cation

def rel_mole_weight(cation, cation_num, oxy_num):
    """calculate the relative molecular mass of the formula

    :param cation: cation
    :param cation_num: the number of the cation
    :param oxy_num: the number of the oxygen atom
    :return: the relative molecular mass
    """
    length = len(cation)
    if length != len(cation_num) or length != len(oxy_num):
        raise Exception

    relative_molecular_weight = []
    for i in range(length):
        a = ION_DICT[cation[i]] * cation_num[i] + ION_DICT['O'] * oxy_num[i]
        relative_molecular_weight.append(a)
    return relative_molecular_weight

def normalization_factor_calculation(rmw, oxy_num, data_input, model=1):
    """calculate the normalization factor

    :param rmw: relative molecular mass
    :param oxy_num: the number of the oxygen atom
    :param data_input: dataset
    :return: the value of normalization factor in every raw
    """
    normalization_factor = []
    data_num = data_input.shape[0]
    if model == 1 or model == 2:
        anion_coef = 12
    elif model == 3:
        anion_coef = 6
    for i in range(data_num):
        single_data = data_input.iloc[i, :]
        nf = float(anion_coef) / sum(np.array(oxy_num) * np.array(single_data) / np.array(rmw))
        normalization_factor.append(nf)
    return normalization_factor

def cation_formula_calculation(normalization_factor, rmw, cation_num, data, ion):
    """calculate the value of the formula of cations

    :param normalization_factor: normalization factor
    :param rmw: relative molecular weight
    :param cation_num: the number of cation
    :param data: dataset
    :param ion: the name of cation
    :return: the value of the formula of cations
    """
    data_num = data.shape[0]
    cation = []
    for j in range(data_num):
        single_data = data.iloc[j, :]
        cation_formula = normalization_factor[j] * np.array(single_data) * np.array(cation_num) / np.array(rmw)
        cation.append(cation_formula)
    cation_df = pd.DataFrame(cation)
    cation_df.columns = ion
    return cation_df

def zero2minimum(single_data):
    """change the value which is zero into 0.0000001

    :param single_data: data point
    :return: data which may be 0.0000001
    """
    single_data = 0.0000001 if single_data == 0 else single_data
    return single_data

def transform(data):
    """replace the data value in the sheet if it is zero

    :param data: data set
    :return: data set without zero
    """
    data_transformed = data.applymap(zero2minimum)
    return data_transformed

def result2sheet(df, df_name=None, model=1):
    """make a sheet to store the result

    :param df: dataset
    :param model: pattern
    :return: a sheet for storing
    """
    if df_name == None:
        if model == 1 or model == 2:
            df_name = "cpx_cation_data"
        elif model == 3:
            df_name = "spl_cation_data"
    try:
        # drop the index in case that the dimensions change
        df.to_excel("{}.xlsx".format(df_name), index=False)
        print("Successfully store the results of {} in '{}.xlsx' \n".format(df_name, df_name))
    except ModuleNotFoundError:
        print("** Please download openpyxl by pip3 **")
        print("** The data will be stored in .csv file **")
        df.to_csv("{}.csv".format(df_name))
        print("Successfully store the results of {} in '{}.csv' \n".format(df_name, df_name))

def poly_preprocess(data, option):
    """increase data dimensions for polynomial regression

    :param data: data set
    :param option:  pattern to indicate which .pkl to use
    :return: augmented data
    """
    # different patterns have different pkl
    if option == 1:
        model = PCA_MODEL[0]
    elif option == 2:
        model = PCA_MODEL[1]
    pca_path = os.path.join(WORKING_PATH, MODEL_PATH, model)
    pca_model = joblib.load(pca_path)
    # do dimension reduction first
    data_reduced = pca_model.fit_transform(data)
    # afterwards do feature augmentation
    poly_features = PolynomialFeatures(degree=POLY_DEGREE, include_bias=False)
    data_augmented = poly_features.fit_transform(data_reduced)
    return data_augmented

def tree_preprocess(data):
    """increase data dimensions for tree-based model like extra tree

    :param data: data set
    :return: augmented data set
    """
    new_dimension = data['Na'] / data['Mg']
    data['Na/Mg'] = new_dimension
    return data

def range_limit(y):
    """limit predicted value in the range of 0 to 1,

    :param y: predicted value
    :return: limited predicted value
    """
    list_y = list(y)
    # negative will be replaced with 0, greater than 1 will be replaced with 1
    for i in range(len(list_y)):
        if list_y[i] > 1:
            list_y[i] = 1
        elif list_y[i] < 0:
            list_y[i] = 0
    return np.array(list_y)

def model_relaunch(option, model_name, model, data):
    """relaunch trained model with specific pattern

    :param option: one of the three patterns
    :param model_name: the name of ML models
    :param model: machine learning model
    :param data: data set used for predicting
    :return: data set with the prediction results
    """
    data_temp = data.copy()
    # loop and relaunch the model with user's data set
    for i in range(len(model_name)):
        joblib_model = joblib.load(os.path.join(WORKING_PATH, MODEL_PATH, model[i]))
        # polynomial reg and tree model are special because of data dimensions
        if model_name[i] == 'Polynomial Regression':
            data_augmented = poly_preprocess(data_temp, option)
            y = joblib_model.predict(data_augmented)
            # limit the predicted value in the range of 0 to 1
            y_limited = range_limit(y)
        elif model_name[i] == 'Extra Tree' or model_name[i] == 'Random Forest':
            if option == 1 or option == 2:
                data_augmented = tree_preprocess(data_temp)
            elif option == 3:
                # data dimension don't change in model 3
                data_augmented = data_temp
            y = joblib_model.predict(data_augmented)
            y_limited = range_limit(y)
        else:
            y = joblib_model.predict(data_temp)
            y_limited = range_limit(y)
        print("{} is predicting ......".format(model_name[i]))
        print("Prediction Values: ")
        print(y_limited)
        data[model_name[i]] = y_limited
        print("The results has been appended to the cation data set")
        print("." * 20 + '\n')
    return data


