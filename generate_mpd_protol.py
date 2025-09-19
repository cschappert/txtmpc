# generate_mpd_protocol.py
import inspect
from mpd import MPDClient

def get_mpd_commands(cls: type):
    """Collect all command names registered on the class."""
    commands = set()
    for name, attr in inspect.getmembers(cls):
        # Only look for methods that were added as commands
        if hasattr(attr, "__self__") and attr.__self__ is cls:
            continue  # skip bound methods
        if hasattr(attr, "__func__"):
            func = attr.__func__
        else:
            func = attr
        if hasattr(func, "mpd_commands"):
            for cmd in func.mpd_commands:
                commands.add(cmd.replace(" ", "_"))
    # Also check for dynamically added methods
    for name in dir(cls):
        if not name.startswith("_") and callable(getattr(cls, name)):
            commands.add(name)
    return sorted(commands)

def generate_protocol(commands: list[str], protocol_name="MPDCommandsProtocol") -> str:
    lines = [
        "from typing import Protocol, Any, Iterator, Dict, Optional, Union",
        "",
        f"class {protocol_name}(Protocol):"
    ]
    for cmd in commands:
        lines.append(f"    def {cmd}(self, *args: Any, **kwargs: Any) -> Any: ...")
    return "\n".join(lines)

if __name__ == "__main__":
    commands = get_mpd_commands(MPDClient)
    protocol_code = generate_protocol(commands)
    with open("mpd_protocols.py", "w") as f:
        f.write(protocol_code)
    print("Protocol written to mpd_protocols.py")
