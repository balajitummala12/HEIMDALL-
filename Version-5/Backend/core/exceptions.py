"""
Custom Exceptions for HEIMDALL
"""

class HeimdallError(Exception):
    """Base exception."""
    pass


class AIError(HeimdallError):
    pass


class VoiceError(HeimdallError):
    pass


class MemoryError(HeimdallError):
    pass


class SearchError(HeimdallError):
    pass


class PluginError(HeimdallError):
    pass