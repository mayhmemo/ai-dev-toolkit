def get_operational_system():
    import platform

    system = platform.system()
    if system == 'Darwin':
        return f"macOS {platform.mac_ver()[0]}"
    elif system == 'Linux':
        try:
            with open('/etc/os-release') as f:
                for line in f:
                    if line.startswith('PRETTY_NAME='):
                        return line.split('=')[1].strip().strip('"')
        except (IOError, IndexError):
            pass
        return 'Linux'
    elif system == 'Windows':
        return platform.win32_ver()[0]
    return system

def get_file_tree(directory: str, file_extensions: list[str] | None = None):
    if file_extensions is None:
        file_extensions = ["*.md", "*.py", "*.ipynb"]
        
    find_command = " -o ".join(f"-name '{ext}'" for ext in file_extensions)
    return find_command

