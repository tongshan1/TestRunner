from flask import Blueprint

api = Blueprint('views', __name__)

from . import InterfaceManager
from . import ModuleManager
from . import ProjectManager
from . import TestCaseGroupManager
from . import ReportManager
from . import SystemManager
from . import Timer
from . import Index
