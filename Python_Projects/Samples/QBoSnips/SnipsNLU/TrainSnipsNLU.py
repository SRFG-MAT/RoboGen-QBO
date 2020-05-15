import io
import json

from snips_nlu import SnipsNLUEngine
from snips_nlu.default_configs import CONFIG_DE

engine = SnipsNLUEngine(config=CONFIG_DE)
with io.open("dataset.json") as f:
    dataset = json.load(f)

engine.fit(dataset)
engine.persist("QBo_Model")
