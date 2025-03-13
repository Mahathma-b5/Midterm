"""App Testing"""
from unittest.mock import patch
import pytest
from app import App

def test_app_get_environment_variable():
    """App Testing for Env Varaibles"""
    with patch("builtins.input", return_value="exit"):
        app = App(start_repl=False)
        current_env = app.get_environment_variable('ENVIRONMENT')
        assert current_env in ['DEVELOPMENT',
                               'TESTING', 'PRODUCTION'],f"Invalid ENVIRONMENT: {current_env}"



def test_app_start_exit_command(monkeypatch):
    """Test that the REPL exits correctly on 'exit' command."""
    monkeypatch.setattr('builtins.input', lambda _: 'exit')
    with pytest.raises(SystemExit) as exit_info:
        app = App(start_repl=False)  # Prevent REPL auto-start
        app.run_repl()
    assert str(exit_info.value) == "Exiting..."
