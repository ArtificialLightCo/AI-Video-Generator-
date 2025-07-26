# backend/plugin_manager.py
import os
import subprocess
import pkg_resources
import xmlrpc.client

class PluginManager:
    """
    Discover and install plugins from PyPI or GitHub.
    """
    def __init__(self, plugin_dir='plugins'):
        self.plugin_dir = plugin_dir
        os.makedirs(self.plugin_dir, exist_ok=True)

    def list_local(self) -> list:
        """
        List plugin scripts in plugins directory.
        """
        return [f[:-3] for f in os.listdir(self.plugin_dir) if f.endswith('.py')]

    def list_installed(self) -> list:
        """
        List installed packages that look like plugins.
        """
        return [d.project_name for d in pkg_resources.working_set if 'plugin' in d.project_name.lower()]

    def search_pypi(self, query: str) -> list:
        """
        Search PyPI for plugin packages matching the query.
        """
        client = xmlrpc.client.ServerProxy('https://pypi.org/pypi')
        results = client.search({'summary': query}, 'or')
        # return top 10 package names
        return [r['name'] for r in sorted(results, key=lambda x: -int(x.get('downloads', 0)))][:10]

    def install_plugin(self, name: str) -> bool:
        """
        Install a plugin via pip.
        """
        subprocess.run(['pip', 'install', name], check=True)
        return True
