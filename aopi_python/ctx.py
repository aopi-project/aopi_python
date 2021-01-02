from pathlib import Path

from aopi_index_builder import get_context
from starlette.templating import Jinja2Templates

context = get_context()
plugin_dir = Path(__file__).parent
templates_dir = plugin_dir / "templates"
templates = Jinja2Templates(directory=templates_dir)
