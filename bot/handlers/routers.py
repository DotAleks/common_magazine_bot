from .user.commands import router as user_commands_router
from .user.catalog import router as user_catalog_router

routers = [user_commands_router, user_catalog_router]