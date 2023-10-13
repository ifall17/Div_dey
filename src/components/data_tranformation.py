import sys
import os
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.impute import SimpleImputer

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object

@dataclass
class DataTransformationConfig:
    prepro_obj_file_path = os.path.join("artifacts","preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        """
        Cette fonction est responsable de la
        transformation des donnees

        """

        try:

            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                    "gender",
                    "race_ethnicity",
                    "parental_level_of_education",
                    "lunch",
                    "test_preparation_course",
                ]

            num_pipeline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),

                    ("scaler",StandardScaler())
                ]
            )

            cat_pipeline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder()),
                    ("scaler",StandardScaler(with_mean=False))
                ]
            )

            logging.info("Encodage Colonnes categorielles complet ")

            prepro = ColumnTransformer(
                [
                    ("num_pipeline",num_pipeline,numerical_columns),
                    ("cat_pipeline",cat_pipeline,categorical_columns)
                ]
            )

            return prepro
        except Exception as e:
            raise CustomException(e,sys)


    def initiate_dt_trans(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            prepo_obj = self.get_data_transformer_object()

            target_col_name = "math_score"

            feature_train = train_df.drop(columns=[target_col_name],axis=1)
            target_train = train_df[target_col_name]

            feature_test= test_df.drop(columns=[target_col_name],axis=1)
            target_test = test_df[target_col_name]

            input_feature_train_arr = prepo_obj.fit_transform(feature_train)
            input_feature_test_arr = prepo_obj.transform(feature_test)

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_train)
                    ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_test)]

            logging.info(f"Saved preprocessing object.")

            save_object(

            file_path=self.data_transformation_config.prepro_obj_file_path,
            obj=prepo_obj

                )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.prepro_obj_file_path,
            )

        except Exception as e:
            raise CustomException(e,sys)