import pytest
from unittest.mock import patch, mock_open, MagicMock
from ai_dev_toolkit.utils.misc.utils import get_operational_system, get_file_tree

@patch('platform.system')
@patch('platform.mac_ver')
def test_get_operational_system_macos(mock_mac_ver, mock_system):
    mock_system.return_value = 'Darwin'
    mock_mac_ver.return_value = ('10.15.7', '', '')
    assert get_operational_system() == 'macOS 10.15.7'

@patch('platform.system')
@patch('builtins.open')
def test_get_operational_system_linux(mock_open, mock_system):
    mock_system.return_value = 'Linux'
    mock_open.return_value.__enter__.return_value = [
        'PRETTY_NAME="Ubuntu 20.04 LTS"\n'
    ]
    assert get_operational_system() == 'Ubuntu 20.04 LTS'

@patch('platform.system')
@patch('builtins.open')
def test_get_operational_system_linux_no_pretty_name(mock_open, mock_system):
    mock_system.return_value = 'Linux'
    mock_open.return_value.__enter__.return_value = [
        'NAME="Ubuntu"\n',
        'VERSION="20.04 LTS"\n'
    ]
    assert get_operational_system() == 'Linux'

@patch('platform.system')
@patch('builtins.open')
def test_get_operational_system_linux_io_error(mock_open, mock_system):
    mock_system.return_value = 'Linux'
    mock_open.side_effect = IOError()
    assert get_operational_system() == 'Linux'

@patch('platform.system')
@patch('builtins.open')
def test_get_operational_system_linux_index_error(mock_open, mock_system):
    mock_system.return_value = 'Linux'
    mock_line = MagicMock()
    mock_line.split.side_effect = IndexError()
    mock_line.startswith.return_value = True
    mock_open.return_value.__enter__.return_value = [mock_line]
    assert get_operational_system() == 'Linux'

@patch('platform.system')
@patch('platform.win32_ver')
def test_get_operational_system_windows(mock_win32_ver, mock_system):
    mock_system.return_value = 'Windows'
    mock_win32_ver.return_value = ('10', '', '', '')
    assert get_operational_system() == '10'

@patch('platform.system')
def test_get_operational_system_unknown(mock_system):
    mock_system.return_value = 'Unknown'
    assert get_operational_system() == 'Unknown'

def test_get_file_tree_default():
    result = get_file_tree("/some/path")
    assert "-name '*.md' -o -name '*.py' -o -name '*.ipynb'" in result

def test_get_file_tree_custom_extensions():
    result = get_file_tree("/some/path", [".txt", ".json"])
    assert "-name '.txt' -o -name '.json'" in result

def test_get_file_tree_single_extension():
    result = get_file_tree("/some/path", [".txt"])
    assert "-name '.txt'" in result
    assert "-o" not in result 