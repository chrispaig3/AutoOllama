from ollama import RequestError, ResponseError, create
from loguru import logger


name: str = input("Choose a name for your model: ")
model_selection: str = input("Select a model to train: ")
prompt: str = input("Enter a prompt to train the model with: ")
  

modelfile: str = f"""
FROM {model_selection}
SYSTEM {prompt}
"""


class Model:
    def __init__(self, name, modelfile) -> None:
        self.name = name
        self.modelfile = modelfile

    @staticmethod
    def init() -> None:
        try:
            model: Model = Model(name, modelfile) 
            create(model=model.name, modelfile=model.modelfile)            
            
            logger.info(f"Generated Model: {model.name}")
        except (RuntimeError, RequestError, ResponseError) as e:
            logger.debug(e)


if __name__ == "__main__":
    Model.init()
