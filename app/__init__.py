"""
App package initialization.

Provides a simple greeting function used throughout the project
and by the test suite.
"""

def greet(name: str = "World") -> str:
    """
    Return a friendly greeting message.

    Parameters
    ----------
    name : str, optional
        The name to include in the greeting. Defaults to "World".

    Returns
    -------
    str
        Greeting string in the format ``"Hello, {name}!"``.
    """
    return f"Hello, {name}!"