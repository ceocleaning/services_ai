import pluggy

# Create hook specification and implementation markers
hookspec = pluggy.HookspecMarker("services_ai")
hookimpl = pluggy.HookimplMarker("services_ai")

# Export for use in other modules
__all__ = ['hookspec', 'hookimpl']
