"""cc00_langchain — runnable enterprise-grade examples for the LangChain ecosystem.

Companion to core-component-00/telescope/2026-07-25-langchain-ecosystem-assessment/supporting/.
See ../../README.md for what is actually tested versus reference-only.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("cc00-enterprise-examples")
except PackageNotFoundError:  # not installed as a package, running from source
    __version__ = "0.0.0+source"
