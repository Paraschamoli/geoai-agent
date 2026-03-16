# |---------------------------------------------------------|
# |                                                         |
# |                 Give Feedback / Get Help                |
# | https://github.com/getbindu/Bindu/issues/new/choose    |
# |                                                         |
# |---------------------------------------------------------|
#
#  Thank you users! We ❤️ you! - 🌻

"""geoai-agent - An Bindu Agent."""

from geoai_agent.__version__ import __version__
from geoai_agent.main import (
    handler,
    initialize_agent,
    main,
)

__all__ = [
    "__version__",
    "handler",
    "initialize_agent",
    "main",
]
