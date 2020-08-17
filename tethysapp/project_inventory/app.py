from tethys_sdk.base import TethysAppBase, url_map_maker
from tethys_sdk.app_settings import CustomSetting, PersistentStoreDatabaseSetting
from tethys_sdk.permissions import Permission, PermissionGroup


class ProjectInventory(TethysAppBase):
    """
    Tethys app class for Project Inventory.
    """

    name = 'Project Inventory'
    index = 'project_inventory:home'
    icon = 'project_inventory/images/dam_icon.png'
    package = 'project_inventory'
    root_url = 'project-inventory'
    color = '#244C96'
    description = ''
    tags = ''
    enable_feedback = False
    feedback_emails = []

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (
            UrlMap(
                name='home',
                url='project-inventory',
                controller='project_inventory.controllers.home'
            ),
            UrlMap(
                name='add_project',
                url='project-inventory/projects/add',
                controller='project_inventory.controllers.add_project'
            ),
            UrlMap(
                name='projects',
                url='project-inventory/projects',
                controller='project_inventory.controllers.list_projects'
            ),
        )

        return url_maps

    def custom_settings(self):
        """
        Example custom_settings method.
        """
        custom_settings = (
            CustomSetting(
                name='max_projects',
                type=CustomSetting.TYPE_INTEGER,
                description='Maximum number of projects that can be created in the app.',
                required=False
            ),
        )

        return custom_settings

    def persistent_store_settings(self):
        """
        Define Persistent Store Settings.
        """
        ps_settings = (
            PersistentStoreDatabaseSetting(
                name='primary_db',
                description='primary database',
                initializer='project_inventory.model.init_primary_db',
                required=True
            ),
        )

        return ps_settings

    def permissions(self):
        """
        Define permissions for the app.
        """
        add_projects = Permission(
            name='add_projects',
            description='Add projects to inventory'
        )

        admin = PermissionGroup(
            name='admin',
            permissions=(add_projects,)
        )

        permissions = (admin,)

        return permissions
