import unittest
from unittest.mock import patch, MagicMock
import sys
import io

# Add project root to path
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import show_welcome

class TestShowWelcome(unittest.TestCase):
    def test_show_welcome_with_rich(self):
        """Test that show_welcome imports rich and prints a panel."""
        with patch.dict('sys.modules', {'rich.console': MagicMock(), 'rich.panel': MagicMock(), 'rich.text': MagicMock()}):
            # Mock the Console class
            mock_console_class = MagicMock()
            mock_console_instance = mock_console_class.return_value

            with patch('rich.console.Console', mock_console_class):
                result = show_welcome()

                self.assertTrue(result)
                mock_console_class.assert_called_once()
                mock_console_instance.print.assert_called_once()

    def test_show_welcome_without_rich(self):
        """Test that show_welcome returns False if rich is not available."""
        with patch.dict('sys.modules', {'rich': None}):
            with patch('builtins.__import__', side_effect=ImportError):
                # We need to ensure the import fails inside the function
                # Since 'rich' might be already imported, we reload or use patch
                # Ideally, we mock the import mechanism for 'rich'
                pass

        # A simpler way to test ImportError handling is to mock the specific import statement or ensure it raises ImportError
        # Since the import is inside the function, we can patch `rich.console` to raise ImportError when accessed?
        # No, because the import happens at function scope.

        # Let's try patching builtins.__import__ specifically for 'rich'
        original_import = __import__
        def mock_import(name, *args, **kwargs):
            if name.startswith('rich'):
                raise ImportError("No module named 'rich'")
            return original_import(name, *args, **kwargs)

        with patch('builtins.__import__', side_effect=mock_import):
            # We also need to clear sys.modules for rich if it's there
            with patch.dict('sys.modules'):
                keys_to_remove = [k for k in sys.modules if k.startswith('rich')]
                for k in keys_to_remove:
                    del sys.modules[k]

                result = show_welcome()
                self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
