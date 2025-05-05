from .exec_command import ExecuteCommandStrategy
from .api_command import ApiCallStrategy

# Create a mapping of command names to strategy classes
COMMAND_STRATEGIES = {
    "exec": ExecuteCommandStrategy,
    "api": ApiCallStrategy
}
