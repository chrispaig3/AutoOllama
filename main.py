import ollama
from loguru import logger
from simple_chalk import chalk, green

name = input(chalk.green.bold("Choose a name for your model: "))
model_selection = input(chalk.green.bold("Select a model to train: "))
prompt = input(chalk.green.bold("Enter a prompt to train the model with: "))
  

modelfile = f"""
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
            model = Model(name, modelfile)
            ollama.create(model=model.name, modelfile=model.modelfile)
            logger.info(f"Generated Model: {model.name}")
        
        except ollama.RequestError as e:
            logger.debug(e)


if __name__ == "__main__":
    Model.init()
