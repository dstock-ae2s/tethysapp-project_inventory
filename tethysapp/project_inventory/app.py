from tethys_sdk.base import TethysAppBase, url_map_maker
from tethys_sdk.app_settings import CustomSetting, PersistentStoreDatabaseSetting
from tethys_sdk.permissions import Permission, PermissionGroup


class ProjectInventory(TethysAppBase):
    """
    Tethys app class for Project Inventory.
    """

    name = 'Watford City Capital Improvements Plan'
    index = 'project_inventory:home'
    icon = 'project_inventory/images/Watford_City_Logo-white.png'
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
                controller='project_inventory.controllers.add_facility'
            ),
            UrlMap(
                name='projects',
                url='project-inventory/projects',
                controller='project_inventory.controllers.list_projects'
            ),
            UrlMap(
                name='get-project-list',
                url='project-inventory/get-project-list',
                controller='project_inventory.ajax_controllers.get_project_list'
            ),
            UrlMap(
                name='get-project-categorized-list',
                url='project-inventory/get-project-categorized-list',
                controller='project_inventory.ajax_controllers.get_project_categorized_list'
            ),
            UrlMap(
                name='revenue',
                url='project-inventory/revenue',
                controller='project_inventory.controllers.list_revenue'
            ),
            UrlMap(
                name='save-updates-to-db',
                url='project-inventory/save-updates-to-db',
                controller='project_inventory.ajax_controllers.save_updates_to_db'
            ),
            UrlMap(
                name='save-cat-updates-to-db',
                url='project-inventory/save-cat-updates-to-db',
                controller='project_inventory.ajax_controllers.save_cat_updates_to_db'
            ),
            UrlMap(
                name='graphs',
                url='project-inventory/graphs',
                controller='project_inventory.controllers.graphs'
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