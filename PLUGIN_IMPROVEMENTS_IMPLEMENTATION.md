# 🚀 Plugin System Improvements - Implementation Guide

## Priority Features

1. ✅ **Dependency Management** - Auto-install plugin dependencies
2. ✅ **Sandboxing** - Restrict module imports for security  
3. ✅ **Error Handling** - Comprehensive logging & auto-disable
4. ✅ **Plugin SDK** - Developer tools & templates

---

## 1️⃣ Dependency Management

### Add to manifest.json:
```json
{
  "dependencies": {
    "packages": {
      "requests": ">=2.28.0",
      "pandas": "^1.5.0"
    }
  }
}
```

### New Model:
```python
class PluginDependency(models.Model):
    plugin = ForeignKey(Plugin)
    package_name = CharField(max_length=100)
    version_spec = CharField(max_length=50)
    install_status = CharField(choices=['pending', 'installed', 'failed'])
```

### New File: `plugins/dependency_manager.py`
- Creates virtualenv per plugin
- Installs packages with pip
- Adds to sys.path when loading

---

## 2️⃣ Sandboxing

### New File: `plugins/sandbox.py`
```python
class PluginImportRestriction:
    SAFE_MODULES = {'json', 'datetime', 'math', 're'}
    BLOCKED = {'os', 'sys', 'subprocess', 'socket'}
    
    # Only allow imports from manifest dependencies
```

### Usage:
```python
with PluginSandbox(plugin):
    # Plugin code runs here
    # Blocked imports raise ImportError
```

---

## 3️⃣ Error Handling

### New Models:
```python
class PluginError(models.Model):
    plugin, error_type, hook_name
    error_message, stack_trace
    occurred_at, resolved
    
class PluginExecutionLog(models.Model):
    plugin, hook_name
    execution_time, success
```

### Auto-disable after 5 consecutive errors
### Notify admins on errors
### Track execution time per hook

---

## 4️⃣ Plugin SDK

### CLI Tool:
```bash
# Create new plugin
services-ai-plugin create my-plugin

# Validate manifest
services-ai-plugin validate

# Test plugin
services-ai-plugin test

# Package for upload
services-ai-plugin package
```

### Base Class:
```python
from services_ai_sdk import ServicesAIPlugin

class MyPlugin(ServicesAIPlugin):
    def lead_created(self, lead, context, api):
        # Your code here
```

---

## 📋 Implementation Order

### Week 1: Dependency Management
1. Add PluginDependency model
2. Create DependencyManager class
3. Update upload view
4. Test with requests package

### Week 2: Sandboxing
1. Create PluginImportRestriction
2. Create PluginSandbox context manager
3. Update plugin_manager.py
4. Test import blocking

### Week 3: Error Handling
1. Add error models
2. Create PluginErrorHandler
3. Update call_hook with safe_hook_execution
4. Add admin notifications

### Week 4: SDK
1. Create base plugin class
2. Build CLI tool
3. Create templates
4. Write documentation

---

## 🎯 Benefits

### Dependency Management:
- ✅ Plugins can use any Python package
- ✅ Isolated environments (no conflicts)
- ✅ Automatic installation

### Sandboxing:
- ✅ Prevents malicious imports
- ✅ Whitelist approach (safe by default)
- ✅ Only allow declared dependencies

### Error Handling:
- ✅ Track all errors with stack traces
- ✅ Auto-disable problematic plugins
- ✅ Admin notifications
- ✅ Performance monitoring

### SDK:
- ✅ Easy plugin development
- ✅ Templates & examples
- ✅ Testing tools
- ✅ Validation before upload

---

Full detailed implementation in separate files per feature.
