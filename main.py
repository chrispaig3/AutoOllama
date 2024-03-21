from os import system
from sqlite3 import connect, Error as SQLError
from ollama import RequestError, ResponseError, create
from loguru import logger


DB_PATH: str = "db/models.db"


name: str = input("Choose a name for your model: ")
model_selection: str = input("Select a model to train: ")
prompt: str = input("Enter a prompt to train the model with: ")
backup: str = input("Would you like to backup this model? (y/n/restore): ")  


system("clear")


modelfile: str = f"""
FROM {model_selection}
SYSTEM {prompt}
"""


def create_backup() -> None:
    try:       
        conn = connect(DB_PATH)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS models (name TEXT, modelfile TEXT);")
        c.execute("INSERT INTO models VALUES (?, ?);", (name, modelfile))
        conn.commit()
    except SQLError as e:
        logger.error(e)
    finally:
        conn.close()     


def restore_models() -> None:
    try:
        conn = connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM models;")
        models = c.fetchall()
        for model in models:
            create(model=model[0], modelfile=model[1])
            logger.info(f"Restored Model: {model[0]}")
    except SQLError as e:
        logger.error(e)
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
            logger.error(e)
        finally:
            match backup:
                case "y":
                    create_backup()
                    logger.info(f"Backup created for Model: {name}") 
                case "n":
                    logger.info("No backup created")
                case "restore":
                    logger.info("Restoring backup...")
                    restore_models()
                    exit(0)
                case _:
                    logger.error("No backup created. Invalid input, exiting...")
                    exit(1)
                    

if __name__ == "__main__":
    Model.init()
