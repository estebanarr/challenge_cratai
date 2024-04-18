from fastapi import Depends
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from app.entitites import (
    InputText,
    Response
)
from app.config import Settings, get_settings
from pandas import (
                        DataFrame
                    )
from typing import Union, List
import structlog
import pickle
import gzip
import warnings
from joblib import load
from sklearn.feature_extraction.text import TfidfVectorizer


warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

logger = structlog.get_logger()
router = InferringRouter()


@cbv(router)
class Evaluator:
    settings: Settings = Depends(get_settings)
    api_version = open("app/version.txt", "r").readline().rstrip()

    try:
        with gzip.open("ml_models/" + get_settings().model_name, "rb") as file:
            
            model = pickle.load(file)

        with gzip.open("ml_models/" + get_settings().vectorizer_name, "rb") as file:
            
            vectorizer = pickle.load(file)

        logger.info("Model loaded correctly")

    except Exception as e:
        logger.error("Error loading model")
        raise

    @router.post("/analyze")
    async def analyze_text(self, text_description: InputText):

        logger.info(f"Text received: {text_description}")
        text =" ".join(text_description.text_description)
        text = [text]

        X = self.vectorizer.transform(text)

        # Get DataFrame to be used in Modeling

        data_model = DataFrame(X.toarray(), columns=self.vectorizer.get_feature_names())

        print(data_model)

        logger.debug("Input transformed", data_model)
        prediccion= self.model.predict_proba(data_model)
        prob_label_0 = prediccion[0][1]
        prob_label_1 = prediccion[0][1]
        prediction_class = str(prediccion[0][1] > 0.025518)

        print(prediction_class)
    

        resp = Response(
            prob_label_0=prob_label_0,
            prob_label_1=prob_label_1,
            prediction_class=prediction_class,
            api_version=self.api_version,
            model_version=self.settings.model_name,
        )

        return resp



