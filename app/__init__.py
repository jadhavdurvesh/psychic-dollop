"""Top-level package for the application."""

def greet(name: str = "World") -> str:
    """
    Return a friendly greeting message.

    Parameters
    ----------
    name : str, optional
        Name to include in the greeting. Defaults to "World".

    Returns
    -------
    str
        Greeting string.
    """
    return f"Hello, {name}!"

__all__ = ["greet"]