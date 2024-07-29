from pathlib import Path

from beacon import load_config

config_file = Path(__file__).parent / "../conf/config.molgenis.yml"

load_config(config_file.as_posix())
