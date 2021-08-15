from typing import Dict, Any
from injectark import FactoryBuilder
from .base_factory import BaseFactory
from .check_factory import CheckFactory
from .cloud_factory import CloudFactory
from .directory_factory import DirectoryFactory
from .http_factory import HttpFactory
from .sql_factory import SqlFactory


factory_builder = FactoryBuilder([
    BaseFactory, CheckFactory, CloudFactory,
    DirectoryFactory, HttpFactory, SqlFactory])
