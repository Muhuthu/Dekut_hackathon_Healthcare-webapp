from workspace import create_app

if __name__ == "__main__":
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    from imblearn.over_sampling import SMOTENC
    import pandas as pd
    import numpy as np
    
    """# Import dataset"""
    DATA_PATH = "/home/muhuthu/Documents/medic_kit_hackathon/workspace/dataset/breast_mammogram_dataset.csv"
    df = pd.read_csv(DATA_PATH)
    
    """# Preprocessing"""
    
    #Remove all row with missing bmi_c (bmi_c == -99)
    df = df.drop(df[df['bmi_c']==-99.0].index, )

    #Duplicate sample with assess_c == 5 
    df= df._append(df[df['assess_c']==5].iloc[0:2,] )
    df= df._append(df[df['assess_c']==5].iloc[0:2,] )

    #Split feature to target
    X = df.drop(['assess_c'],axis=1)
    y = df['assess_c']

    #Remove irrelevant columns
    cols_to_drop = {'cancer_c','compfilm_c','CaTypeO','ptid'}
    X.drop(columns=cols_to_drop, inplace=True)

    # Numerical features
    numerical_features = ['age_c','bmi_c']

    # Categorical features for X
    categorical_features = [col for col in X.columns if (col not in numerical_features)]

    # Categorical features index
    categorical_features_index = [X.columns.to_list().index(categorical_features[i]) for i in range(len(categorical_features)) ]

    # Dataset is very unbalanced : use [SMOTE] with categorical variables
    oversample = SMOTENC(categorical_features=categorical_features_index)
    col_tmp = X.columns
    X, y = oversample.fit_resample(X, y)

    X = pd.DataFrame(X, columns=col_tmp)

    for feature in categorical_features:
        X[feature] = X[feature].astype('category')

    #Save min and max of numerical variables
    #global min_age
    min_age = X['age_c'].min()
    
    #global max_age 
    max_age = X['age_c'].max()

    #global min_bmi
    min_bmi = X['bmi_c'].max()

    #global max_bmi
    max_bmi = X['bmi_c'].min() 

    # Preprocessing for numerical features : Normalize same as Standard Scaler
    for feature in numerical_features:
        #X[feature] = (X[feature] - np.min(X[feature])) / (np.max(X[feature]) - np.min(X[feature]))
        X[feature] = X[feature]/100

    # Preprocessing for categorical features : same as OneHotEncoder
    X = pd.get_dummies(X)

    # Split training samples and test samples
    x_train, x_test, y_train, y_test = train_test_split(X,y,test_size = 0.2,random_state=0)
    
    """## Random Forest"""
    #global model
    model = RandomForestClassifier(n_estimators=1000, random_state=1)
   
    #global model
    model.fit(x_train,y_train)
    #model.fit(X,y)

    
    
    app = create_app()
    app.run(debug=True)