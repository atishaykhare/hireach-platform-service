import logging
import random
import string
import os
import importlib

logger = logging.getLogger(__name__)
ALPHA_NUM = string.ascii_letters + string.digits


def generate_random_alphanum(length: int = 20) -> str:
    return "".join(random.choices(ALPHA_NUM, k=length))


def include_routers(app, directory):
    # Get a list of all Python files in the specified directory
    files = os.listdir(directory)
    modules = [f.replace('.py', '') for f in files if f.endswith('.py') and not f.startswith('__')]
    directory = directory.replace('/', '.')

    # Dynamically import the router modules and include their routes
    for module in modules:
        module_path = f"{directory}.{module}"
        route_module = importlib.import_module(module_path)
        app.include_router(route_module.router)
