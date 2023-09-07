from sensor.configuration.mongo_db_conn import mongoDBclient
from sensor.exception import SensorException
import sys,os
from sensor.logger import logging
# from sensor.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig
from sensor.pipeline.training_pipeline import TrainingPipeline
from sensor.constant.training_pipeline import SAVED_MODEL_DIR
from sensor.ml.model.estimator import ModelResolver,TargetValueMapping
from sensor.utils.main_utils import load_object

from fastapi import FastAPI
from sensor.constant.application import APP_HOST, APP_PORT
from starlette.responses import RedirectResponse
from uvicorn import run as app_run
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/",tags = ["authentication"])
async def index():
    return RedirectResponse(url = "/docs")

@app.get("/train")
async def train_route():
    try:
        training_pipeline = TrainingPipeline()
        if training_pipeline.is_pipeline_running:
            return Response("Training pipeline is running")
        training_pipeline.run_pipeline()
        return Response("Training successful !!")
    except Exception as e:
        raise Exception(f"Error occurred! {e}")

@app.get("/predict")
async def predict_route():
    try:
        #get data from user csv file
        #conver csv file to dataframe

        df=None
        model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)
        if not model_resolver.is_model_exists():
            return Response("Model is not available")
        
        best_model_path = model_resolver.get_best_model_path()
        model = load_object(file_path=best_model_path)
        y_pred = model.predict(df)
        df['predicted_column'] = y_pred
        df['predicted_column'].replace(TargetValueMapping().reverse_mapping(),inplace=True)
        
        #decide how to return file to user.
    except Exception as e:
        raise Exception(f"Error occurred! {e}")

# def test_exception():
#     try:
#         100/0
#     except Exception as e:
#         raise SensorException(e,sys)
    

def main():
    try:
        training_pipeline = TrainingPipeline()
        training_pipeline.run_pipeline()
    except Exception as e:
        print(e)
        logging.exception(e)


if __name__=="__main__":
    #main()
    # set_env_variable(env_file_path)
    app_run(app, host=APP_HOST, port=APP_PORT)

# if __name__ == "__main__":
    # print("hello")
    # mongo_client = mongoDBclient()
    # print(mongo_client.client.test)
    # print(mongo_client.database.list_collection_names())
    # try:
    #     logging.info("Executing test_exception function")
    #     test_exception()
    #     logging.info("test_exception function executed successfully")
    # except Exception as e:
    #     logging.info(e)
    #     print(e)

    # training_pipeline_config = TrainingPipelineConfig()
    # data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
    # print(data_ingestion_config.__dict__)
