import pathlib
import os
import logging

logging.basicConfig(format="%(levelname)s:%(name)s:%(module)s:%(message)s")
logger = logging.getLogger("pybbda")

_version = "0.2.0"

PYBBDA_LOG_LEVEL_NAME = os.environ.get("PYBBDA_LOG_LEVEL", "")
_PYBBDA_LOG_LEVEL_MAP = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "CRITICAL": logging.CRITICAL,
}

PYBBDA_LOG_LEVEL = logging.INFO
logger.setLevel(logging.INFO)
if PYBBDA_LOG_LEVEL_NAME in _PYBBDA_LOG_LEVEL_MAP:
    logger.info("setting root logger log level to %s", PYBBDA_LOG_LEVEL_NAME)
    PYBBDA_LOG_LEVEL = _PYBBDA_LOG_LEVEL_MAP[PYBBDA_LOG_LEVEL_NAME]
    logger.setLevel(_PYBBDA_LOG_LEVEL_MAP[PYBBDA_LOG_LEVEL_NAME])


def get_pybbda_data_root():
    if os.environ.get("PYBBDA_DATA_ROOT") is not None:
        root_path = pathlib.Path(os.environ.get("PYBBDA_DATA_ROOT"))
    else:
        root_path = pathlib.Path(__file__).absolute().parent / "data" / "assets"
        logger.warning(
            f"Environment variable PYBBDA_DATA_ROOT is not set, "
            f"defaulting to {root_path}"
        )
    return root_path


PYBBDA_DATA_ROOT = get_pybbda_data_root()
