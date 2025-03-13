"""Main application module for calculator REPL interface."""
import importlib
import logging
import os
import pkgutil
from typing import Dict
from dotenv import load_dotenv # type: ignore
from app.commands import Command, CommandHandler
import logging
import logging.config
class App:
    """Main application class handling initialization, 
        plugin loading, and REPL execution."""
    def __init__(self, start_repl=True):
        """Initialize application components and environment."""
        self.load_environment()        
        self.setup_logging()        
        self.logger = logging.getLogger(__name__)
        self.logger.info("Application is Starting")
        self.command_handler = CommandHandler()
        self.load_plugins()
        self.logger.info("Application initialized")
        if start_repl:
            self.run_repl()
        

    def setup_logging(self):
        """Configure logging using environment variables."""
        log_level = self.settings.get('LOG_LEVEL', 'INFO').upper()
        log_output = self.settings.get('LOG_OUTPUT', './logs/app.log')

        # Ensure the log directory exists
        log_directory = os.path.dirname(log_output)
        os.makedirs(log_directory, exist_ok=True)

        numeric_level = getattr(logging, log_level, logging.INFO)

        logging.basicConfig(
            level=numeric_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.handlers.RotatingFileHandler(
                    filename=log_output,
                    maxBytes=1048576,
                    backupCount=5
                )
            ]
        )

        # Test logger to confirm configuration loaded successfully
        test_logger = logging.getLogger("setup_test")
        test_logger.info("Logging configured successfully with level %s at %s", log_level, log_output)

    def load_environment(self):
        """Load environment variables from .env file."""
        try:
            load_dotenv()
            self.settings = dict(os.environ)
            environment = self.get_environment_variable('ENVIRONMENT')  # Specify parameter
            print("Environment variables loaded successfully")
            print(f"Current environment: {environment}")
        except Exception as e:
            print(f"Failed to load environment variables: {str(e)}")
            raise

    def get_environment_variable(self, env_var: str = 'ENVIRONMENT'):
        """
        Retrieve and validate environment variable.
        
        Args:
            env_var: Name of the environment variable to retrieve
            
        Returns:
            Value of the environment variable or empty string if not found
        """
        value = self.settings.get(env_var, None)
        if not value:
            self.logger.warning("Environment variable %s not set", env_var)
        return value

    def load_plugins(self):
        """Discover and register plugin commands from plugins directory."""
        plugins_package = 'app.plugins'
        self.logger.info("Starting plugin loading process")
        if not self._plugins_directory_exists(plugins_package):
            return

        for module_info in pkgutil.iter_modules([plugins_package.replace('.', '/')]):
            if not module_info.ispkg:
                continue
            self._process_plugin_module(plugins_package, module_info.name)

    def _plugins_directory_exists(self, plugins_package: str) -> bool:
        plugins_path = plugins_package.replace('.', '/')
        if not os.path.exists(plugins_path):
            self.logger.error("Plugin directory %s not found", plugins_path)
            return False
        return True

    def _process_plugin_module(self, plugins_package: str, plugin_name: str):
        try:
            plugin_module = importlib.import_module(f'{plugins_package}.{plugin_name}')
            self._register_commands_from_module(plugin_module, plugin_name)
        except Exception as error: # pylint: disable=broad-except
            self.logger.error("Error loading plugin %s: %s", plugin_name, str(error), exc_info=True)

    def _register_commands_from_module(self, plugin_module, plugin_name: str):
        for item_name in dir(plugin_module):
            item = getattr(plugin_module, item_name)
            if not isinstance(item, type) or not issubclass(item, Command) or item == Command:
                continue
            command_instance = item() if item_name != 'MenuCommand' else item(self.command_handler)
            self.command_handler.register_command(plugin_name, command_instance)
            self.logger.info("Registered command: %s", plugin_name)

    def run_repl(self):
        """Run Read-Eval-Print Loop (REPL) interface for user interaction."""
        self.logger.info("Starting REPL interface")
        print("Welcome to Calculator")

        try:
            while True:
                try:
                    user_input = input(">>> ").strip()
                    self.logger.debug("User input: %s", user_input)

                    if user_input.lower() == "exit":
                        self.logger.info("Exit command received")
                        self.command_handler.execute_command("exit")
                        break

                    self._execute_command(user_input)
                except KeyboardInterrupt:
                    self.logger.info("Keyboard interrupt detected")
                    print("\nExiting...")
                    break
        except Exception:
            self.logger.critical("REPL session failed", exc_info=True)
            raise

    def _execute_command(self, user_input: str):
        parts = user_input.split()
        if not parts:
            return

        command_name, args = parts[0], parts[1:]
        if command_name in self.command_handler.commands:
            command = self.command_handler.commands[command_name]
            if callable(command.execute):
                try:
                    command.execute(*args) if args else command.execute()
                except TypeError as e:
                    print(f"Error: {e}")
            else:
                print("Command is not executable")
        else:
            print(f"No such command: {command_name}")
