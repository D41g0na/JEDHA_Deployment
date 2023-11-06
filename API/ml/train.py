import mlflow
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import  OneHotEncoder, StandardScaler 
from sklearn.compose import ColumnTransformer
from xgboost import XGBRegressor
from mlflow.models.signature import infer_signature

if __name__ == "__main__":

    # Set your variables for your environment
    EXPERIMENT_NAME="getaround_pricing"

    #Instanciate your experiment
    client = mlflow.tracking.MlflowClient()

    mlflow.set_tracking_uri("file://./mlruns")

    # Set experiment's info 
    mlflow.set_experiment(EXPERIMENT_NAME)
    # Get our experiment info
    experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)

    print("training model...")

    # Call mlflow autolog
    mlflow.sklearn.autolog(log_models=False)

    df = pd.read_csv("API/data/train_dataset.csv")
  
    # Separate target variable Y from features X
    target_name = 'rental_price_per_day'
    Y = df.loc[:,target_name]
    X = df.drop(target_name, axis = 1)

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    numeric_features = []
    categorical_features = []
    for i,t in X.dtypes.items():
        if ('float' in str(t)) or ('int' in str(t)) :
            numeric_features.append(i)
        else :
            categorical_features.append(i)
    
    numeric_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())
        ])

    categorical_transformer = Pipeline(steps=[
        ('encoder', OneHotEncoder(drop='first', handle_unknown='ignore'))
        ])
    
    preprocessor = ColumnTransformer(transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
        ])
    
    model = Pipeline(steps=[
        ("Preprocessing", preprocessor),
        ("Regressor", XGBRegressor())
        ])
    
    with mlflow.start_run(experiment_id = experiment.experiment_id):

        model.fit(X_train, Y_train)

        predictions = model.predict(X_train)
        
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="price_car",
            registered_model_name="price_car_model",
            signature=infer_signature(X_train, predictions)
        )

    print("...Done!")

    