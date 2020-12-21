import os

# basic oxides needed to calculate the cation data
CPX_OXIDE = ['SiO2', 'TiO2', 'Al2O3', 'Cr2O3', 'FeO', 'MnO', 'MgO', 'CaO', 'Na2O']
SPL_OXIDE = ['SiO2', 'TiO2', 'Al2O3', 'Cr2O3', 'FeO', 'MnO', 'NiO', 'MgO']

# cation needed for model's prediction
CPX_ION = ['Si', 'Ti', 'Al', 'Cr', 'Fe', 'Mn', 'Mg', 'Ca', 'Na']
SPL_ION = ['Si', 'Ti', 'Al', 'Cr', 'Fe', 'Mn', 'Ni', 'Mg']

# fill the missing value of user's data set with a specific value
NULL2VALUE = 0

# the dictionary of relative atomic mass
ION_DICT = {'Si': 28.085, 'Ti': 47.867, 'Al': 26.981, 'Cr': 51.996, 'Fe': 55.845, 'Mn': 54.938,
            'Mg': 24.305, 'Ca': 40.078, 'Na': 22.989, 'K': 39.098, 'P': 30.974, 'Ni': 58.693,
            'Zn': 65.390, 'Li': 6.941, 'Zr': 91.224, 'V': 50.941, 'O': 15.999}

# current package path
WORKING_PATH = os.getcwd()

# the directory where trained models are stored
MODEL_PATH = os.path.join('pyroxene_processor','trained_model')

# trained model
MODEL_NAME_ONE = ['Polynomial Regression', 'Artificial Neutral Network', 'Extra Tree', 'Random Forest']
MODEL_ONE = ['poly.pkl', 'mlp.pkl', 'et.pkl', 'rf.pkl']
MODEL_NAME_TWO = ['Linear Regression', 'Polynomial Regression', 'Extra Tree', 'Random Forest']
MODEL_TWO = ['Linear_new.pkl', 'poly_new.pkl', 'et_new.pkl', 'rf_new.pkl']
MODEL_NAME_THREE = ['Linear Regression', 'Extra Tree']
MODEL_THREE = ['Linear_spl.pkl', 'et_spl.pkl']

# trained pca model
PCA_MODEL = ['pca.pkl', 'pca_new.pkl']

# the degree for polynomial regression
POLY_DEGREE = 3
