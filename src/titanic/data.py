"""
Load, preprocess, prepare, and save the Titanic dataset.
"""
import os
import pandas as pd
from prefect import flow, task
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from titanic.registry import load_model, save_model
from titanic.params import DATA_FOLDER,NUMERIC_FEATURES,CAT_FEATURES

@task
def load_data(train: bool = True) -> pd.DataFrame:
    """
    Load the Titanic dataset from a CSV file.
    
    Returns:
        DataFrame: The loaded Titanic dataset.
    """
    if not os.path.exists(DATA_FOLDER):
        raise FileNotFoundError(f"The data folder '{DATA_FOLDER}' does not exist.")
    # Without ternary operator
    # if train == True : 
    #     name = 'train'
    # else:
    #     name = 'test'
    # Using ternary operator for brevity
    name = 'train' if train else 'test'
    # df = pd.read_csv(os.path.join(DATA_FOLDER, f'{name}.csv'),index_col='PassengerId')
    df = pd.read_csv("https://storage.googleapis.com/schoolofdata-datasets/titanic-train.csv")
    if not train :
        y_test = pd.read_csv(os.path.join(DATA_FOLDER,"gender_submission.csv"), index_col='PassengerId')
        df = pd.merge(df,y_test,left_index=True, right_index=True, how='left')
    return df
@task
def clean_data(df):
    """
    clean the Titanic dataset.
    
    Args:
        df (DataFrame): The Titanic dataset.
        
    Returns:
        DataFrame: The preprocessed Titanic dataset.
    """
    
    return    df.drop(columns=['Name', 'Ticket', 'Cabin'])\
                .dropna()\
                .drop_duplicates()
        
@task
def prepare_data(df:pd.DataFrame ,fit=True, survive=True) -> tuple[pd.DataFrame, pd.Series]: 
    """
    Prepare the Titanic dataset for training.
    
    Args:
        df (DataFrame): The cleaned Titanic dataset.
        
    Returns:
        tuple: A tuple containing [X,y] the features DataFrame and the target Series.
    """
    if survive:
        X,y = df.drop(columns=['Survived']), df['Survived']
    else:
        X, y = df, None
    if fit :
        numeric_transformer = Pipeline(steps=[
                                            ('imputer', SimpleImputer(strategy='mean')),
                                            ('scaler', StandardScaler())
                                        ])  
        cat_pipeline = Pipeline(steps=[
                                            ('imputer', SimpleImputer(strategy='most_frequent')),
                                            ('encoder', OneHotEncoder(sparse_output=False, handle_unknown='ignore', drop='first'))
                                        ])
        preprocessor = ColumnTransformer(
                                            transformers=[
                                                ('num', numeric_transformer, NUMERIC_FEATURES),
                                                ('cat', cat_pipeline, CAT_FEATURES)
                                            ],
                                            remainder='passthrough'  # Keep other columns as they are
                                        ).set_output(transform="pandas")
        preprocessor.fit(X)
        save_model(preprocessor, "preprocessor.pkl")
    else:
        preprocessor = load_model("preprocessor.pkl")
    X_scaled = preprocessor.transform(X)
    return X_scaled, y

@flow(name="titanic_data_pipeline")
def titanic_data_pipeline(train: bool = True) -> tuple[pd.DataFrame, pd.Series]:
    """
    Main flow to load, clean, and prepare the Titanic dataset.
    
    Args:
        train (bool): Whether to load the training dataset or the test dataset.
        
    Returns:
        tuple: A tuple containing [X,y] the features DataFrame and the target Series.
    """
    df = load_data(train)
    df = clean_data(df)
    X, y = prepare_data(df)
    return X, y

if __name__ == "__main__":
    # Example usage
    # df = load_data(train=False)
    # print(df.shape)
    # df = clean_data(df)
    # X, y = prepare_data(df)
    # print(X.head())
    # print(y.head())

    titanic_data_pipeline(train=True)
    
    # # Save the processed data
    # X.to_csv('titanic_features.csv', index=False)
    # y.to_csv('titanic_target.csv', index=False)