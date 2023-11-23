#config.py

import connexion
import pathlib

#Set up connexion
basedir = pathlib.Path(__file__).parent.resolve()
connexion_app = connexion.App(__name__, specification_dir=basedir)
