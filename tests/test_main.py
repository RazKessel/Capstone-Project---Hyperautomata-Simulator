import pytest
from unittest.mock import patch, MagicMock
from main import main

@patch("main.DBManager")
@patch("main.tk.Tk")
@patch("main.LoginWindow")
def test_main(mock_login_window, mock_tk, mock_db_manager):
    """Test the main function."""
    # Mock objects
    mock_db_instance = MagicMock()
    mock_db_manager.return_value = mock_db_instance

    mock_tk_instance = MagicMock()
    mock_tk.return_value = mock_tk_instance

    mock_login_window_instance = MagicMock()
    mock_login_window.return_value = mock_login_window_instance

    # Run the main function
    with patch("sys.exit") as mock_exit:
        main()

    # Assertions
    mock_db_manager.assert_called_once_with(db_url="sqlite:///automata.db")
    mock_tk.assert_called_once()
    # Verify LoginWindow was called with the actual callback
    mock_login_window.assert_called_once()
    call_args = mock_login_window.call_args.kwargs
    assert call_args["parent"] == mock_tk_instance
    assert call_args["db_manager"] == mock_db_instance
    assert callable(call_args["success_callback"])
