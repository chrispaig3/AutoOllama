import sqlite3
from ollama import RequestError, ResponseError, create
from loguru import logger


name: str = input("Choose a name for your model: ")
model_selection: str = input("Select a model to train: ")
prompt: str = input("Enter a prompt to train the model with: ")
backup = input("Would you like to backup the model? (y/n): ")  


modelfile: str = f"""
FROM {model_selection}
SYSTEM {prompt}
"""

  
def create_backup() -> None:
    try:
        conn = sqlite3.connect("db/models.db")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS models (name TEXT, modelfile TEXT);")
        c.execute("INSERT INTO models VALUES (?, ?);", (name, modelfile))
        conn.commit()
    except sqlite3.Error as e:
        logger.debug(f"Error: {e}")
    finally:
        conn.close()


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
            logger.debug(f"Error: {e}")
        finally:
            if backup == "y":
                create_backup()
                logger.info(f"Backup created for Model: {name}")              


if __name__ == "__main__":
    Model.init()
