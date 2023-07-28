import functools
from typing import Any, Callable, Dict, Optional, Set
import warnings


class FunctionWrapper:
    """Function wrapper"""

    def __init__(self, func: Callable[..., Any]) -> None:
        self.func = func
        self._aliases: Set[str] = set()


class alias(object):
    """Add an alias to a function"""

    def __init__(self, *aliases: str, deprecated_version: str = None) -> None:
        """Constructor

        Args:
            deprecated_version (str, optional): Version number that deprecation will happen. Defaults to None.
        """
        self.aliases: Set[str] = set(aliases)
        self.deprecated_version: Optional[str] = deprecated_version

    def __call__(self, f: Callable[..., Any]) -> FunctionWrapper:
        """call"""
        wrapped_func = FunctionWrapper(f)
        wrapped_func._aliases = self.aliases

        @functools.wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Alias wrapper"""
            if self.deprecated_version:
                aliases_str = ", ".join(self.aliases)
                msg = f"{aliases_str} is deprecated and will be removed in version {self.deprecated_version}. Use {f.__name__} instead."
                warnings.warn(msg, DeprecationWarning)
            return f(*args, **kwargs)

        wrapped_func.func = wrapper  # Assign wrapper directly to func attribute
        return wrapped_func


def aliased(aliased_class: Any) -> Any:
    """Class has aliases"""
    original_methods: Dict[str, Any] = aliased_class.__dict__.copy()
    for name, method in original_methods.items():
        if isinstance(method, FunctionWrapper) and hasattr(method, "_aliases"):
            for alias in method._aliases:
                setattr(aliased_class, alias, method.func)

            # Also replace the original method with the wrapped function
            setattr(aliased_class, name, method.func)

    return aliased_class
