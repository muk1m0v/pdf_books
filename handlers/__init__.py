from .admin import router as admin_router
from .common import router as common_router
from .student import router as student_router


routers = (common_router, student_router, admin_router)
