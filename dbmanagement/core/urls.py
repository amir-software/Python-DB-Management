from .storage_management import services as storage_services

from django.urls import path


urlpatterns = [
    path('v1/repository_manager/', storage_services.RepositoryManager.as_view()),
    path('v1/persist_table/', storage_services.PersistTable.as_view()),
]