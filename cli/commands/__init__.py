from .api_command import ApiCallStrategy
from .exec_command import ExecuteCommandStrategy
from .get_command import GetCommandStrategy
from .refresh_command import RefreshCommandStrategy
from .update_command import UpdateCommandStrategy

# Create a mapping of command names to strategy classes
COMMAND_STRATEGIES = {
    "exec": ExecuteCommandStrategy,
    "api": ApiCallStrategy,
    "get": GetCommandStrategy,
    "update": UpdateCommandStrategy,
    "refresh": RefreshCommandStrategy,
}
