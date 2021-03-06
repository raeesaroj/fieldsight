from rest_framework import permissions

from onadata.apps.fieldsight.models import Project
from .models import ReportSettings


class ReportingProjectFormsPermissions(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to View it.
    """

    def has_object_permission(self, request, view, obj):
        if request.is_super_admin:
            return True

        project = obj.project

        if project is not None:
            organization_id = project.organization_id
            user_role_org_admin = request.roles.filter(organization_id=organization_id,
                                                       group__name="Organization Admin")

            if user_role_org_admin:
                return True

            user_role_as_manager = request.roles.filter(project_id=project.id, group__name__in=["Project Manager",
                                                                                                "Project Donor"])

            if user_role_as_manager:
                return True

        return False

    def has_permission(self, request, view):

        if request.is_super_admin:
            return True

        project_id = view.kwargs.get('pk', None)

        project = Project.objects.get(id=project_id)

        if project is not None:
            organization_id = project.organization_id
            user_role_org_admin = request.roles.filter(organization_id=organization_id,
                                                       group__name="Organization Admin")

            if user_role_org_admin:
                return True

            user_role_as_manager = request.roles.filter(project_id=project.id, group__name__in=["Project Manager",
                                                                                                "Project Donor"])

            if user_role_as_manager:
                return True

        return False


class ReportingSettingsPermissions(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to create/edit it.
    """

    def has_permission(self, request, view):

        if request.is_super_admin:
            return True

        obj = ReportSettings.objects.get(id=view.kwargs.get('pk', None))

        project = obj.project

        if project is not None:
            organization_id = project.organization_id
            user_role_org_admin = request.roles.filter(organization_id=organization_id,
                                                       group__name="Organization Admin")

            if user_role_org_admin:
                return True

            user_role_as_manager = request.roles.filter(project_id=project.id, group__name__in=["Project Manager",
                                                                                                "Project Donor"])

            if user_role_as_manager:
                return True

        return False