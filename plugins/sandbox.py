"""
Plugin Sandboxing System

Restricts module imports to prevent malicious code execution.
"""

import sys
import importlib.abc


class PluginImportRestriction(importlib.abc.MetaPathFinder):
    """Restrict imports for plugin code"""
    
    # Safe standard library modules
    SAFE_STDLIB = {
        'json', 'datetime', 'time', 'math', 'random', 'decimal',
        'collections', 'itertools', 'functools', 'operator',
        're', 'string', 'textwrap', 'copy', 'typing',
        'enum', 'dataclasses', 'abc', 'contextlib',
        'hashlib', 'hmac', 'base64', 'uuid',
    }
    
    # Dangerous modules that are always blocked
    BLOCKED_MODULES = {
        'os', 'sys', 'subprocess', 'shutil', 'glob',
        'importlib', '__builtin__', 'builtins',
        'socket', 'ssl', 'http', 'urllib', 'urllib3',
        'ftplib', 'telnetlib', 'smtplib',
        'pickle', 'marshal', 'shelve',
        'ctypes', 'cffi', 'pty', 'tty',
        'signal', 'resource', 'gc',
    }
    
    # Django modules (whitelist specific parts)
    SAFE_DJANGO = {
        'django.http', 'django.shortcuts', 'django.utils',
        'django.template', 'django.forms',
    }
    
    def __init__(self, plugin_id, allowed_packages=None):
        self.plugin_id = plugin_id
        self.allowed_packages = allowed_packages or set()
        self.active = False
    
    def find_spec(self, fullname, path, target=None):
        """Check if module import is allowed"""
        if not self.active:
            return None
        
        # Get root module name
        root_module = fullname.split('.')[0]
        
        # Check if blocked
        if root_module in self.BLOCKED_MODULES:
            raise ImportError(
                f"[SANDBOX] Plugin {self.plugin_id}: Import of '{fullname}' is blocked (security restriction)"
            )
        
        # Check if it's a safe stdlib module
        if root_module in self.SAFE_STDLIB:
            return None  # Allow default import
        
        # Check if it's a safe Django module
        if any(fullname.startswith(safe) for safe in self.SAFE_DJANGO):
            return None  # Allow default import
        
        # Check if it's in plugin's declared dependencies
        if root_module in self.allowed_packages:
            return None  # Allow default import
        
        # Block everything else
        raise ImportError(
            f"[SANDBOX] Plugin {self.plugin_id}: Import of '{fullname}' is not allowed. "
            f"Add '{root_module}' to 'dependencies.packages' in manifest.json"
        )
    
    def __enter__(self):
        """Enable import restrictions"""
        self.active = True
        sys.meta_path.insert(0, self)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Disable import restrictions"""
        self.active = False
        if self in sys.meta_path:
            sys.meta_path.remove(self)


class PluginSandbox:
    """Sandbox environment for plugin execution"""
    
    def __init__(self, plugin):
        self.plugin = plugin
        self.import_hook = None
    
    def get_allowed_packages(self):
        """Get list of packages plugin is allowed to import"""
        manifest = self.plugin.manifest
        dependencies = manifest.get('dependencies', {})
        packages = dependencies.get('packages', {})
        
        # Return package names (without version specs)
        return set(packages.keys())
    
    def __enter__(self):
        """Enter sandbox context"""
        allowed_packages = self.get_allowed_packages()
        self.import_hook = PluginImportRestriction(
            plugin_id=self.plugin.id,
            allowed_packages=allowed_packages
        )
        self.import_hook.__enter__()
        
        print(f"[SANDBOX] Enabled for plugin {self.plugin.name}")
        if allowed_packages:
            print(f"[SANDBOX] Allowed packages: {', '.join(allowed_packages)}")
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit sandbox context"""
        if self.import_hook:
            self.import_hook.__exit__(exc_type, exc_val, exc_tb)
        
        print(f"[SANDBOX] Disabled for plugin {self.plugin.name}")
