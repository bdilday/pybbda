import pathlib
import os
import logging

logging.basicConfig(format = '%(levelname)s:%(module)s:%(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_pybbda_data_root():
    if os.environ.get("PYBBDA_DATA_ROOT") is not None:
        root_path = pathlib.Path(os.environ.get("PYBBDA_DATA_ROOT"))
    else:
        root_path = pathlib.Path(__file__).absolute().parent / "data" / "assets"
        logger.warning(
            f"Environment variable PYBBDA_DATA_ROOT is not set, defaulting to {root_path}"
        )
    return root_path


PYBBDA_DATA_ROOT = get_pybbda_data_root()

