from typing import Any

from invoice_router.runtime import InvoiceRouterRuntime, build_runtime

__all__ = ["InvoiceRouterRuntime", "app", "build_runtime", "create_app"]
__version__ = "0.1.0"


def __getattr__(name: str) -> Any:
    if name in {"app", "create_app"}:
        from invoice_router.api import app, create_app

        return {"app": app, "create_app": create_app}[name]
    raise AttributeError(name)
