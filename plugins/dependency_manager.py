"""
Dependency Manager for Services AI Plugins

Manages plugin dependencies in isolated virtual environments.
"""

import subprocess
import sys
from pathlib import Path
import venv


class DependencyManager:
    """Manage plugin dependencies in isolated environments"""
    
    def __init__(self, plugin):
        self.plugin = plugin
        self.plugin_dir = Path(plugin.package_path)
        self.venv_dir = self.plugin_dir / 'venv'
        self.pip_path = self.venv_dir / 'bin' / 'pip'
    
    def create_virtualenv(self):
        """Create isolated virtualenv for plugin"""
        if self.venv_dir.exists():
            print(f"[DEPS] Virtualenv already exists for {self.plugin.name}")
            return True
        
        try:
            print(f"[DEPS] Creating virtualenv for {self.plugin.name}")
            venv.create(self.venv_dir, with_pip=True, system_site_packages=False)
            return True
        except Exception as e:
            print(f"[DEPS] Error creating virtualenv: {e}")
            return False
    
    def parse_dependencies(self):
        """Parse dependencies from manifest"""
        manifest = self.plugin.manifest
        dependencies = manifest.get('dependencies', {})
        packages = dependencies.get('packages', {})
        
        return packages
    
    def install_dependencies(self):
        """Install all plugin dependencies"""
        from plugins.models import PluginDependency
        
        # Create virtualenv
        if not self.create_virtualenv():
            return False
        
        # Parse dependencies
        packages = self.parse_dependencies()
        
        if not packages:
            print(f"[DEPS] No dependencies for {self.plugin.name}")
            return True
        
        success = True
        for package_name, version_spec in packages.items():
            # Create or update dependency record
            dep, created = PluginDependency.objects.get_or_create(
                plugin=self.plugin,
                package_name=package_name,
                defaults={'version_spec': version_spec}
            )
            
            if not created:
                dep.version_spec = version_spec
                dep.save()
            
            # Install package
            if not self.install_package(dep):
                success = False
        
        return success
    
    def install_package(self, dependency):
        """Install a single package"""
        from django.utils import timezone
        
        dependency.install_status = 'installing'
        dependency.save()
        
        try:
            # Build pip install command
            package_spec = f"{dependency.package_name}{dependency.version_spec}"
            
            print(f"[DEPS] Installing {package_spec} for {self.plugin.name}")
            
            # Run pip install in virtualenv
            result = subprocess.run(
                [str(self.pip_path), 'install', package_spec],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                # Get installed version
                installed_version = self.get_installed_version(dependency.package_name)
                
                dependency.install_status = 'installed'
                dependency.installed_version = installed_version
                dependency.installed_at = timezone.now()
                dependency.install_error = None
                dependency.save()
                
                print(f"[DEPS] Successfully installed {dependency.package_name} {installed_version}")
                return True
            else:
                dependency.install_status = 'failed'
                dependency.install_error = result.stderr
                dependency.save()
                
                print(f"[DEPS] Failed to install {dependency.package_name}: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            dependency.install_status = 'failed'
            dependency.install_error = "Installation timeout (5 minutes)"
            dependency.save()
            return False
        except Exception as e:
            dependency.install_status = 'failed'
            dependency.install_error = str(e)
            dependency.save()
            return False
    
    def get_installed_version(self, package_name):
        """Get installed version of a package"""
        try:
            result = subprocess.run(
                [str(self.pip_path), 'show', package_name],
                capture_output=True,
                text=True
            )
            
            for line in result.stdout.split('\n'):
                if line.startswith('Version:'):
                    return line.split(':', 1)[1].strip()
            
            return None
        except Exception:
            return None
    
    def check_dependencies(self):
        """Check if all dependencies are installed"""
        from plugins.models import PluginDependency
        
        deps = PluginDependency.objects.filter(plugin=self.plugin)
        
        all_installed = True
        for dep in deps:
            if dep.install_status != 'installed':
                all_installed = False
                print(f"[DEPS] Missing: {dep.package_name} {dep.version_spec}")
        
        return all_installed
    
    def uninstall_dependencies(self):
        """Uninstall all plugin dependencies (remove virtualenv)"""
        import shutil
        
        if self.venv_dir.exists():
            try:
                shutil.rmtree(self.venv_dir)
                print(f"[DEPS] Removed virtualenv for {self.plugin.name}")
                return True
            except Exception as e:
                print(f"[DEPS] Error removing virtualenv: {e}")
                return False
        
        return True
    
    def get_site_packages_path(self):
        """Get site-packages path for plugin's virtualenv"""
        # Find site-packages in virtualenv
        lib_dir = self.venv_dir / 'lib'
        if lib_dir.exists():
            for python_dir in lib_dir.iterdir():
                if python_dir.name.startswith('python'):
                    site_packages = python_dir / 'site-packages'
                    if site_packages.exists():
                        return str(site_packages)
        return None
