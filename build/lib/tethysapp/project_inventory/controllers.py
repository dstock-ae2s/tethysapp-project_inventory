from django.utils.html import format_html
from django.contrib import messages
from django.shortcuts import render, reverse, redirect
from tethys_sdk.permissions import login_required
from tethys_sdk.gizmos import (Button, MapView, TextInput, DatePicker, 
                               SelectInput, DataTableView, MVDraw, MVView,
                               MVLayer)
import os
from tethys_sdk.permissions import permission_required, has_permission
from .model import Project, Revenue, add_new_project, get_all_projects,get_all_revenue
from .app import ProjectInventory as app
from tethys_sdk.workspaces import app_workspace
from .helpers import *
from tethys_gizmos.gizmo_options import PlotlyView
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json
import numpy as np


# @login_required()
@app_workspace
def home(request, app_workspace):
    """
    Controller for the app home page.
    """



    # Get list of projects and create projects MVLayer:
    projects = get_all_projects()
    ww_features = []
    w_features = []
    sw_features = []
    fac_features = []
    golf_features = []
    transp_features = []
    lat_list = []
    lng_list = []

    for project in projects:
        if project.latitude != 0 and project.longitude != 0:
            lat_list.append(project.latitude)
            lng_list.append(project.longitude)

            project_feature = {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [project.longitude, project.latitude],

                },
                'properties': {
                    'id': project.id,
                    'facility_id': project.facility_id,
                    'project': project.project,
                    'est_cost': project.est_cost,
                    'const_year': project.const_year,
                    'category': project.category,
                    'description': project.description,
                    'priority': project.priority,
                    'est_year': project.est_year,
                    'const_cost': project.const_cost
                }
            }

            if project.category == "Wastewater":
                ww_features.append(project_feature)
            elif project.category == "Stormwater":
                sw_features.append(project_feature)
            elif project.category == "Facilities":
                fac_features.append(project_feature)
            elif project.category == "Golf":
                golf_features.append(project_feature)
            elif project.category == "Transportation":
                fac_features.append(project_feature)
            else:
                w_features.append(project_feature)



    new_file_path = os.path.join(app_workspace.path, "icon.gif")
    print(app_workspace.path)

    # Define GeoJSON FeatureCollections
    sw_projects_feature_collection = {
        'type': 'FeatureCollection',
        'crs': {
            'type': 'name',
            'properties': {
                'name': 'EPSG:4326'
            }
        },
        'features': sw_features
    }
    w_projects_feature_collection = {
        'type': 'FeatureCollection',
        'crs': {
            'type': 'name',
            'properties': {
                'name': 'EPSG:4326'
            }
        },
        'features': w_features
    }
    ww_projects_feature_collection = {
        'type': 'FeatureCollection',
        'crs': {
            'type': 'name',
            'properties': {
                'name': 'EPSG:4326'
            }
        },
        'features': ww_features
    }
    fac_projects_feature_collection = {
        'type': 'FeatureCollection',
        'crs': {
            'type': 'name',
            'properties': {
                'name': 'EPSG:4326'
            }
        },
        'features': fac_features
    }
    golf_projects_feature_collection = {
        'type': 'FeatureCollection',
        'crs': {
            'type': 'name',
            'properties': {
                'name': 'EPSG:4326'
            }
        },
        'features': golf_features
    }
    transp_projects_feature_collection = {
        'type': 'FeatureCollection',
        'crs': {
            'type': 'name',
            'properties': {
                'name': 'EPSG:4326'
            }
        },
        'features': transp_features
    }

    # sw_style = {'ol.style.Style': {
    #     'image': {'ol.style.RegularShape': {
    #         'radius': 10,
    #         'points': 4,
    #         'angle': np.pi / 4,
    #         'fill': {'ol.style.Fill': {
    #             'color':  '#03fc45'
    #         }},
    #         'stroke': {'ol.style.Stroke': {
    #             'color': '#ffffff',
    #             'width': 1
    #         }}
    #     }}
    # }}
    sw_style = {'ol.style.Style': {
        'image': {'ol.style.Icon': {
            'src': '/static/project_inventory/images/Stormwater.png',
            'scale': 0.09,
            # 'points': 4,
            # 'angle': np.pi / 4,
            # 'fill': {'ol.style.Fill': {
            #     'color': '#03fc45'
            # }},
            # 'stroke': {'ol.style.Stroke': {
            #     'color': '#ffffff',
            #     'width': 1
        }},

    }}

    fac_style = {'ol.style.Style': {
        'image': {'ol.style.Icon': {
            'src': '/static/project_inventory/images/facilities.png',
            'scale': 0.09,
            # 'points': 4,
            # 'angle': np.pi / 4,
            # 'fill': {'ol.style.Fill': {
            #     'color': '#03fc45'
            # }},
            # 'stroke': {'ol.style.Stroke': {
            #     'color': '#ffffff',
            #     'width': 1
        }},

    }}

    ww_style = {'ol.style.Style': {
        'image': {'ol.style.Icon': {
            'src': '/static/project_inventory/images/WW.png',
            'scale': 0.09,
            # 'points': 4,
            # 'angle': np.pi / 4,
            # 'fill': {'ol.style.Fill': {
            #     'color': '#03fc45'
            # }},
            # 'stroke': {'ol.style.Stroke': {
            #     'color': '#ffffff',
            #     'width': 1
        }},

    }}
    w_style = {'ol.style.Style': {
        'image': {'ol.style.Icon': {
            'src': '/static/project_inventory/images/Water.png',
            'scale': 0.09,
            # 'points': 4,
            # 'angle': np.pi / 4,
            # 'fill': {'ol.style.Fill': {
            #     'color': '#03fc45'
            # }},
            # 'stroke': {'ol.style.Stroke': {
            #     'color': '#ffffff',
            #     'width': 1
        }},

    }}
    golf_style = {'ol.style.Style': {
        'image': {'ol.style.Icon': {
            'src': '/static/project_inventory/images/Golf.png',
            'scale': 0.09,
            # 'points': 4,
            # 'angle': np.pi / 4,
            # 'fill': {'ol.style.Fill': {
            #     'color': '#03fc45'
            # }},
            # 'stroke': {'ol.style.Stroke': {
            #     'color': '#ffffff',
            #     'width': 1
        }},

    }}
    transp_style = {'ol.style.Style': {
        'image': {'ol.style.Icon': {
            'src': '/static/project_inventory/images/Transportation.png',
            'scale': 0.09,
            # 'points': 4,
            # 'angle': np.pi / 4,
            # 'fill': {'ol.style.Fill': {
            #     'color': '#03fc45'
            # }},
            # 'stroke': {'ol.style.Stroke': {
            #     'color': '#ffffff',
            #     'width': 1
        }},

    }}
    # w_style = {'ol.style.Style': {
    #     'image': {'ol.style.Circle': {
    #         'radius': 10,
    #         'fill': {'ol.style.Fill': {
    #             'color': '#d84e1f'
    #         }},
    #         'stroke': {'ol.style.Stroke': {
    #             'color': '#ffffff',
    #             'width': 1
    #         }}
    #     }}
    # }}

    # ww_style = {'ol.style.Style': {
    #     'image': {'ol.style.RegularShape': {
    #         'radius': 10,
    #         'points': 3,
    #         'rotation': np.pi / 4,
    #         'angle': 0,
    #         'fill': {'ol.style.Fill': {
    #             'color': '#fc0303'
    #         }},
    #         'stroke': {'ol.style.Stroke': {
    #             'color': '#ffffff',
    #             'width': 1
    #         }}
    #     }}
    # }}

    # fac_style = {'ol.style.Style': {
    #     'image': {'ol.style.Circle': {
    #         'radius': 10,
    #         'fill': {'ol.style.Fill': {
    #             'color': '#fcba03'
    #         }},
    #         'stroke': {'ol.style.Stroke': {
    #             'color': '#ffffff',
    #             'width': 1
    #         }}
    #     }}
    # }}

    # golf_style = {'ol.style.Style': {
    #     'image': {'ol.style.Circle': {
    #         'radius': 10,
    #         'fill': {'ol.style.Fill': {
    #             'color': '#a6a49f'
    #         }},
    #         'stroke': {'ol.style.Stroke': {
    #             'color': '#ffffff',
    #             'width': 1
    #         }}
    #     }}
    # }}

    # transp_style = {'ol.style.Style': {
    #     'image': {'ol.style.Circle': {
    #         'radius': 10,
    #         'fill': {'ol.style.Fill': {
    #             'color': '#c000fa'
    #         }},
    #         'stroke': {'ol.style.Stroke': {
    #             'color': '#ffffff',
    #             'width': 1
    #         }}
    #     }}
    # }}

    # Create a Map View Layer
    sw_projects_layer = MVLayer(
        source='GeoJSON',
        options=sw_projects_feature_collection,
        legend_title='Stormwater Projects',
        layer_options={'style': sw_style},
        feature_selection=True
    )
    w_projects_layer = MVLayer(
        source='GeoJSON',
        options=w_projects_feature_collection,
        legend_title='Water Projects',
        layer_options={'style': w_style},
        feature_selection=True
    )
    ww_projects_layer = MVLayer(
        source='GeoJSON',
        options=ww_projects_feature_collection,
        legend_title='Wastewater Projects',
        layer_options={'style': ww_style},
        feature_selection=True
    )
    fac_projects_layer = MVLayer(
        source='GeoJSON',
        options=fac_projects_feature_collection,
        legend_title='Facilities Projects',
        layer_options={'style': fac_style},
        feature_selection=True
    )
    golf_projects_layer = MVLayer(
        source='GeoJSON',
        options=golf_projects_feature_collection,
        legend_title='Golf Projects',
        layer_options={'style': golf_style},
        feature_selection=True
    )
    transp_projects_layer = MVLayer(
        source='GeoJSON',
        options=transp_projects_feature_collection,
        legend_title='Transportation Projects',
        layer_options={'style': transp_style},
        feature_selection=True
    )

    # Define view centered on project locations
    # try:
    #     view_center = [sum(lng_list) / float(len(lng_list)), sum(lat_list) / float(len(lat_list))]
    # except ZeroDivisionError:
    view_center = [-103.28, 47.8]

    view_options = MVView(
        projection='EPSG:4326',
        center=view_center,
        zoom=12.5,
        maxZoom=18,
        minZoom=2
    )

    project_inventory_map = MapView(
        height='100%',
        width='100%',
        layers=[sw_projects_layer, w_projects_layer, ww_projects_layer,
                fac_projects_layer, golf_projects_layer, transp_projects_layer],
        basemap=[
            'OpenStreetMap',
            # 'CartoDB',
            # {'CartoDB': {'style': 'dark'}},
            # 'Stamen',
            # 'ESRI'
        ],
        view=view_options,
        # legend=True

    )

    add_project_button = Button(
        display_text='Add Project',
        name='add-project-button',
        icon='glyphicon glyphicon-plus',
        style='success',
        href=reverse('project_inventory:add_project')
    )

    context = {
        'project_inventory_map': project_inventory_map,
        'add_project_button': add_project_button,
        # 'can_add_projects': has_permission(request, 'add_projects')
    }

    return render(request, 'project_inventory/home.html', context)

def export(request):
    """
    Controller for the Export page.
    """
    start_date_input = DatePicker(
        name='start_date',
        display_text='Start Date',
        autoclose=True,
        format='MM d, yyyy',
        start_date='8/24/2020',
        start_view='decade',
        today_button=True,
        attributes={'class': 'date-input'},
    )

    end_date_input = DatePicker(
        name='end_date',
        display_text='End Date',
        autoclose=True,
        format='MM d, yyyy',
        start_date='8/24/2020',
        start_view='decade',
        today_button=True,
    )

    cancel_button = Button(
        display_text='Cancel',
        name='cancel-button',
        icon='glyphicon glyphicon-remove',
        style='danger',
        href=reverse('project_inventory:home')
    )
    submit_button = Button(
        display_text='Submit',
        name='submit-button',
        style='success',
        icon='glyphicon glyphicon-plus',
        href=reverse('project_inventory:home')
    )

    context = {
        'start_date_input': start_date_input,
        'end_date_input': end_date_input,
        'cancel_button': cancel_button,
        'submit_button':submit_button,
        'can_add_projects': has_permission(request, 'add_projects')
    }

    return render(request, 'project_inventory/export.html', context)


# @permission_required('add_projects')
def add_facility(request):
    """
    Controller for the Add Facility page.
    """
    print("In the controller")
    # Default Values
    facility_id = ''
    project = ''
    est_cost = ''
    const_year = ''
    location = ''
    category = ''
    description = ''
    priority = ''
    est_year = ''
    const_cost = ''
    debt_checked = False
    recur_checked = False


    # Errors
    facility_id_error = ''
    project_error = ''
    est_cost_error = ''
    const_year_error = ''
    location_error = ''
    category_error = ''
    description_error = ''
    priority_error = ''
    est_year_error = ''
    const_cost_error = ''

    # Handle form submission
    if request.POST and 'add-button' in request.POST:
        print("In the first if")
        # Get values
        has_errors = False

        facility_id = request.POST.get('facility_id', None)
        location = request.POST.get('geometry', None)

        # project = (request.POST.get(str(i) + '_add_project_project_name', None))
        # est_cost = (request.POST.get(str(i) + '_add_project_project_estcost', None))
        # est_year = (request.POST.get(str(i) + '_add_project_project_estyear', None))
        # const_cost = (request.POST.get(str(i) + '_add_project_project_constcost', None))
        # const_year =(request.POST.get(str(i) + '_add_project_project_constyear', None))
        # category = (request.POST.get(str(i) + '_add_project_project_category', None))
        # priority = (request.POST.get(str(i) + '_add_project_project_priority', None))
        # description = (request.POST.get(str(i) + '_add_project_project_description', None))
        # debt_checked = (request.POST.get(str(i) + '_add_project_debt_checkbox', None))
        # recur_checked = (request.POST.get(str(i) + '_add_project_recur_checkbox', None))
        project = (request.POST.get('project', None))
        est_cost = (request.POST.get('est_cost', None))
        est_year = (request.POST.get('est_year', None))
        const_cost = (request.POST.get('const_cost', None))
        const_year = (request.POST.get('const_year', None))
        category = (request.POST.get('category', None))
        priority = (request.POST.get('priority', None))
        description = (request.POST.get('description', None))
        debt_checked = (request.POST.get('debt_checkbox', None))
        recur_checked = (request.POST.get('recur_checkbox', None))

        # Validate
        if not facility_id:
            has_errors = True
            facility_id_error = 'Facility ID is required.'

        if not project:
            has_errors = True
            project_error = 'Project Name is required.'

        if not est_cost:
            has_errors = True
            est_cost_error = 'Cost is required.'

        if not const_year:
            has_errors = True
            const_year_error = 'Planned Year is required.'

        if not category:
            has_errors = True
            category_error = 'Category is required.'

        if not description:
            has_errors = True
            description_error = 'Description is required.'

        if not priority:
            has_errors = True
            priority_error = 'Priority is required.'

        if not est_year:
            has_errors = True
            est_year_error = 'Estimate Year is required.'

        if not const_cost:
            has_errors = True
            const_cost_error = 'Construction Cost is required.'

        if not location:
            has_errors = True
            location_error = 'Location is required.'

        if not has_errors:
            print("No Errors")
            # Get value of max_projects custom setting
            max_projects = app.get_custom_setting('max_projects')

            # Query database for count of projects
            Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
            session = Session()
            num_projects = session.query(Project).count()

            # Only add the project if custom setting doesn't exist or we have not exceed max_projects
            if not max_projects or num_projects < max_projects:
                add_new_project(row_id=(num_projects+1), location=location, facility_id=facility_id, project=project, est_cost=est_cost, const_year=const_year, category=category, description=description, priority=priority, est_year=est_year, const_cost=const_cost, debt_checkbox_val=debt_checked, recur_checkbox_val=recur_checked)
                print("Project Added")
            else:
                messages.warning(request, 'Unable to add project "{0}", because the inventory is full.'.format(facility_id))

        else:
            messages.error(request, "Please fix errors.")

        return redirect(reverse('project_inventory:home'))

    # Define form gizmos
    facility_id_input = TextInput(
        display_text='Facility ID',
        name='facility_id',
        initial=facility_id,
        error=facility_id_error
    )

    project_input = TextInput(
        display_text='Project Name',
        name='project',
        initial=project,
        error=project_error
    )

    est_cost_input = TextInput(
        display_text='Estimated Cost',
        name='est_cost',
        attributes={'id':'est_cost',
                    'type':'number'},
        initial=est_cost,
        error=est_cost_error
    )

    description_input = TextInput(
        display_text='Description',
        name='description',
        initial=description,
        error=description_error
    )

    const_cost_input = TextInput(
        display_text='Construction Cost',
        name='const_cost',
        attributes={'id': 'const_cost',
                    'type':'number'},
        initial=const_cost,
        error=const_cost_error
    )

    est_year_input = TextInput(
        display_text='Estimate Year',
        name='est_year',
        attributes={'id': 'est_year',
                    'type':'number'},
        initial=est_year,
        error=est_year_error
    )

    const_year_input = TextInput(
        name='const_year',
        display_text='Construction Year',
        attributes={'id': 'const_year',
                    'type':'number'},
        initial=const_year,
        error=const_year_error
    )

    category_input = SelectInput(
        display_text='Category',
        name='category',
        multiple=False,
        options=[('Water', 'Water'), ('Wastewater', 'Wastewater'), ('Stormwater', 'Stormwater'),
                 ('Facilities', 'Facilities'), ('Golf', 'Golf'), ('Transportation', 'Transportation')],
        initial=['Water'],
        error=category_error
    )

    priority_input = SelectInput(
        display_text='Priority',
        name='priority',
        multiple=False,
        options=[('One', '1'), ('Two', '2'), ('Three', '3'), ('Four', '4'), ('Five', '5')],
        initial=['One'],
        error=priority_error
    )
    view_center = [-103.28, 47.8]
    initial_view = MVView(
        projection='EPSG:4326',
        center=view_center,
        zoom=12.5
    )

    drawing_options = MVDraw(
        controls=['Modify', 'Delete', 'Move', 'Point'],
        initial='Point',
        output_format='GeoJSON',
        point_color='#FF0000'
    )

    location_input = MapView(
        height='300px',
        width='100%',
        basemap=[
            'OpenStreetMap'
            # 'CartoDB',
            # {'CartoDB': {'style': 'dark'}},
            # 'Stamen',
            # 'ESRI'
        ],
        draw=drawing_options,
        view=initial_view
    )

    add_button = Button(
        display_text='Add',
        name='add-button',
        icon='glyphicon glyphicon-plus',
        style='success',
        attributes={'form': 'add-project-form'},
        submit=True
    )

    cancel_button = Button(
        display_text='Cancel',
        name='cancel-button',
        href=reverse('project_inventory:home')
    )

    context = {
        'facility_id_input': facility_id_input,
        'project_input': project_input,
        'est_cost_input': est_cost_input,
        'const_year_input': const_year_input,
        'est_year_input': est_year_input,
        'category_input': category_input,
        'description_input': description_input,
        'priority_input': priority_input,
        'const_cost_input': const_cost_input,
        'location_input': location_input,
        'location_error': location_error,
        'add_button': add_button,
        'cancel_button': cancel_button,
        'can_add_projects': has_permission(request, 'add_projects')
    }

    return render(request, 'project_inventory/add_facility.html', context)


# @login_required()
def list_projects(request):
    """
    Show all projects in a table view.
    """
    projects = get_all_projects()
    table_rows = []

    for project in projects:

        table_rows.append(
            (
                project.facility_id, project.category,
                project.project, project.description, project.priority,
                project.est_year, "$"+"{:,}".format(int(project.est_cost)),
                project.const_year, "$"+"{:,}".format(int(project.const_cost[0])),
                project.debt_checkbox_val, project.recur_checkbox_val,
            )
        )

    projects_table = DataTableView(
        column_names=('Facility ID', 'Category', 'Project', 'Description', 'Priority', 'Estimate Year', 'Estimated Cost', 'Construction Year', 'Construction Cost', 'Debt', 'Recurring'),
        rows=table_rows,
        searching=True,
        orderClasses=False,
        lengthMenu=[[10, 25, 50, -1], [10, 25, 50, "All"]],
    )

    context = {
        'projects_table': projects_table,
        # 'can_add_projects': has_permission(request, 'add_projects')
    }

    return render(request, 'project_inventory/list_projects.html', context)


def list_revenue(request):
    """
    Show all projects in a table view.
    """
    revenues = get_all_revenue()
    table_rows = []

    for revenue in revenues:

        table_rows.append(
            (
                revenue.scenario, revenue.year,
                revenue.revenue_source, "$"+"{:,}".format(round(float(revenue.monetary_Value))),
            )
        )

    revenue_table = DataTableView(
        column_names=('Scenario', 'Year', 'Revenue Source', 'Monetary Value'),
        rows=table_rows,
        searching=True,
        orderClasses=False,
        lengthMenu=[[10, 25, 50, -1], [10, 25, 50, "All"]],
    )

    context = {
        'revenue_table': revenue_table,
    }

    return render(request, 'project_inventory/list_revenue.html', context)




# @login_required()
def capital_costs(request):
    """
    Controller for the Plots Page.
    """
    # Get projects from database
    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()


    bargraph_plot = create_capital_costs_bargraph()
    piechart_plot = create_capital_costs_piechart()
    sunburst_plot = create_capital_costs_sunburst()


    context = {
        'bargraph_plot': bargraph_plot,
        'piechart_plot': piechart_plot,
        'sunburst_plot': sunburst_plot,
        # 'can_add_projects': has_permission(request, 'add_projects')
    }

    session.close()
    return render(request, 'project_inventory/capital_costs.html', context)

def revenue_requirements(request):
    """
    Controller for the Plots Page.
    """
    # Get projects from database
    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()



    bargraph_plot = create_revenue_requirements_bargraph()
    piechart_plot = create_revenue_requirements_piechart()
    sunburst_plot = create_revenue_requirements_sunburst()



    context = {
        'bargraph_plot': bargraph_plot,
        'piechart_plot': piechart_plot,
        'sunburst_plot': sunburst_plot,
        # 'can_add_projects': has_permission(request, 'add_projects')
    }

    session.close()
    return render(request, 'project_inventory/revenue_requirements.html', context)

def revenue(request):
    """
    Controller for the Plots Page.
    """
    # Get projects from database
    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()



    bargraph_low_plot = create_revenue_bargraph("low")
    bargraph_med_plot = create_revenue_bargraph("medium")
    bargraph_high_plot = create_revenue_bargraph("high")
    piechart_low_plot = create_revenue_piechart("low")
    piechart_med_plot = create_revenue_piechart("medium")
    piechart_high_plot = create_revenue_piechart("high")
    # sunburst_plot = create_revenue_sunburst()



    context = {
        'bargraph_low_plot': bargraph_low_plot,
        'bargraph_med_plot': bargraph_med_plot,
        'bargraph_high_plot': bargraph_high_plot,
        'piechart_low_plot': piechart_low_plot,
        'piechart_med_plot': piechart_med_plot,
        'piechart_high_plot': piechart_high_plot,
        # 'sunburst_plot': sunburst_plot,
        # 'can_add_projects': has_permission(request, 'add_projects')
    }

    session.close()
    return render(request, 'project_inventory/revenue.html', context)

def revenue_vs_requirements(request):
    """
    Controller for the Plots Page.
    """

    height = '520px'
    width = '100%'
    """
    Generates a plotly view of projects
    """
    # Get objects from database
    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()
    projects = session.query(Project).all()
    revenue_list = session.query(Revenue).all()

    dfrevreq = pd.DataFrame(columns=['Construction Year', 'Projected Cost', 'Facility ID', 'Project', 'Category'])

    for project in projects:

        if project.debt_checkbox_val == "true":
            z = 1
            for c in range(len(project.const_cost) - 1):
                dfrevreq = dfrevreq.append({'Construction Year': int(project.const_year) + z,
                                            'Projected Cost': float(json.loads(project.const_cost[c + 1])),
                                            'Facility ID': project.facility_id, 'Project': project.project,
                                            'Category': project.category}, ignore_index=True)
                z = z + 1
        elif project.recur_checkbox_val == "true":
            y = 0
            for x in range(len(project.const_cost) - 1):
                dfrevreq = dfrevreq.append({'Construction Year': int(project.const_year) + y,
                                            'Projected Cost': float(json.loads(project.const_cost[x + 1])),
                                            'Facility ID': project.facility_id, 'Project': project.project,
                                            'Category': project.category}, ignore_index=True)
                y = y + 1
        else:
            dfrevreq = dfrevreq.append({'Construction Year': int(project.const_year),
                                        'Projected Cost': float(json.loads(project.const_cost[0])),
                                        'Facility ID': project.facility_id, 'Project': project.project,
                                        'Category': project.category}, ignore_index=True)

    # Build up Plotly plot
    bargraph_high_px = px.bar(
        dfrevreq,
        hover_data=["Facility ID", "Category", "Project", "Projected Cost"],
        x="Construction Year",
        y="Projected Cost",
        color='Category',
        color_discrete_map={
            "Water": "#056eb7",
            "Wastewater": "#b3c935",
            "Existing Debt": "#8065ba",
            "Facilities": "#074768",
            "Golf": "#749f34",
            "Transportation": "#ac162c",
            "Stormwater": "#F78F07"}
        # title="Future Project Costs"
    )

    bargraph_high_px.update_layout(
        yaxis=dict(title='Revenue/Revenue Required (USD)', ),
        xaxis=dict(title='Year'),
        legend=dict(title='Category')
    )

    bargraph_med_px = px.bar(
        dfrevreq,
        hover_data=["Facility ID", "Category", "Project", "Projected Cost"],
        x="Construction Year",
        y="Projected Cost",
        color='Category',
        color_discrete_map={
            "Water": "#056eb7",
            "Wastewater": "#b3c935",
            "Existing Debt": "#001f5b",
            "Facilities": "#074768",
            "Golf": "#ac162c",
            "Transportation": "#232525",
            "Stormwater": "#F78F07"}
        # title="Future Project Costs"
    )

    bargraph_med_px.update_layout(
        yaxis=dict(title='Revenue/Revenue Required (USD)', ),
        xaxis=dict(title='Year'),
        legend=dict(title='Category')
    )

    bargraph_low_px = px.bar(
        dfrevreq,
        hover_data=["Facility ID", "Category", "Project", "Projected Cost"],
        x="Construction Year",
        y="Projected Cost",
        color='Category',
        color_discrete_map={
            "Water": "#056eb7",
            "Wastewater": "#b3c935",
            "Existing Debt": "#001f5b",
            "Facilities": "#074768",
            "Golf": "#ac162c",
            "Transportation": "#232525",
            "Stormwater": "#F78F07"}
        # title="Future Project Costs"
    )

    bargraph_low_px.update_layout(
        yaxis=dict(title='Revenue/Revenue Required (USD)', ),
        xaxis=dict(title='Year'),
        legend=dict(title='Category')
    )

    dfrevhigh = pd.DataFrame(columns=['Scenario', 'Source', 'Monetary Value', 'Year'])
    dfrevmed = pd.DataFrame(columns=['Scenario', 'Source', 'Monetary Value', 'Year'])
    dfrevlow = pd.DataFrame(columns=['Scenario', 'Source', 'Monetary Value', 'Year'])

    for entry in revenue_list:

        if entry.scenario == "high":

            dfrevhigh = dfrevhigh.append({'Scenario': entry.scenario, 'Source': entry.revenue_source,
                                          'Monetary Value': int(json.loads(entry.monetary_Value)),
                                          'Year': int(entry.year)}, ignore_index=True)
        elif entry.scenario == "medium":

            dfrevmed = dfrevmed.append({'Scenario': entry.scenario, 'Source': entry.revenue_source,
                                        'Monetary Value': int(json.loads(entry.monetary_Value)),
                                        'Year': int(entry.year)}, ignore_index=True)
        elif entry.scenario == "low":

            dfrevlow = dfrevlow.append({'Scenario': entry.scenario, 'Source': entry.revenue_source,
                                        'Monetary Value': int(json.loads(entry.monetary_Value)),
                                        'Year': int(entry.year)}, ignore_index=True)

    dfrevhigh_sum = dfrevhigh.groupby("Year").agg(HighRevenue=('Monetary Value', 'sum'))
    dfrevmed_sum = dfrevmed.groupby("Year").agg(MedRevenue=('Monetary Value', 'sum'))
    dfrevlow_sum = dfrevlow.groupby("Year").agg(LowRevenue=('Monetary Value', 'sum'))

    dfrevfinal = pd.DataFrame(columns=["Year"])

    minhyr = dfrevhigh["Year"].min()
    maxhyr = dfrevhigh["Year"].max()

    minmyr = dfrevmed["Year"].min()
    maxmyr = dfrevmed["Year"].max()

    minlyr = dfrevlow["Year"].min()
    maxlyr = dfrevlow["Year"].max()

    maxyr = max(maxlyr,maxmyr,maxhyr)
    minyr = min(minlyr,minmyr,minhyr)

    year_revrange = []

    for i in range(maxyr - minyr + 1):
        year_revrange.append(minyr + i)

    for yearrev in year_revrange:
        dfrevfinal = dfrevfinal.append({'Year': yearrev}, ignore_index=True)

    dfrevfinal = dfrevfinal.merge(dfrevlow_sum, how="left", on="Year")
    dfrevfinal = dfrevfinal.merge(dfrevmed_sum, how="left", on="Year")
    dfrevfinal = dfrevfinal.merge(dfrevhigh_sum, how="left", on="Year")



    bargraph_high_px.add_scatter(y=dfrevfinal["HighRevenue"], x=dfrevfinal["Year"], mode="lines",
                                 line=dict(width=3, color="Red"),
                                 name="High Revenue Scenario")
    bargraph_med_px.add_scatter(y=dfrevfinal["MedRevenue"], x=dfrevfinal["Year"], mode="lines",
                                line=dict(width=3, color="Red"),
                                name="Medium Revenue Scenario")
    bargraph_low_px.add_scatter(y=dfrevfinal["LowRevenue"], x=dfrevfinal["Year"], mode="lines",
                                line=dict(width=3, color="Red"),
                                name="Low Revenue Scenario")


    bargraph_high_plot = PlotlyView(bargraph_high_px, height=height, width=width)
    bargraph_med_plot = PlotlyView(bargraph_med_px, height=height, width=width)
    bargraph_low_plot = PlotlyView(bargraph_low_px, height=height, width=width)


    dfrevreq_rnm = dfrevreq.rename(columns={"Construction Year": "Year"})

    dfrevreq_sum = dfrevreq_rnm.groupby("Year").agg(total_cost=('Projected Cost', 'sum'))

    minfyr = min(int(dfrevreq_rnm["Year"].min()), int(minyr))
    maxfyr = max(int(dfrevreq_rnm["Year"].max()), int(maxyr))

    year_range = []

    for i in range(maxfyr - minfyr + 1):
        year_range.append(minfyr + i)

    dfdiff = pd.DataFrame(columns=["Year", "Difference High", "Difference Medium","Difference Low"])

    for yearf in year_range:
        dfdiff = dfdiff.append({'Year': yearf, "Difference High": 0, "Difference Medium": 0, "Difference Low": 0}, ignore_index=True)

    dfdiff = dfdiff.merge(dfrevfinal, how="left", on="Year")
    dfdiff = dfdiff.merge(dfrevreq_sum, how="left", on="Year")

    dfdiff["HighRevenue"] = dfdiff["HighRevenue"].fillna(0)
    dfdiff["MedRevenue"] = dfdiff["MedRevenue"].fillna(0)
    dfdiff["LowRevenue"] = dfdiff["LowRevenue"].fillna(0)
    dfdiff["total_cost"] = dfdiff["total_cost"].fillna(0)
    dfdiff["Difference High"] = (dfdiff["HighRevenue"] - dfdiff["total_cost"])
    dfdiff["Difference Medium"] = (dfdiff["MedRevenue"] - dfdiff["total_cost"])
    dfdiff["Difference Low"] = (dfdiff["LowRevenue"] - dfdiff["total_cost"])


    dfdiff["High Deficit Or Surplus"] = ["Surplus" if difvalh >= 0 else "Deficit" for difvalh in dfdiff["Difference High"]]
    dfdiff["Medium Deficit Or Surplus"] = ["Surplus" if difvalm >= 0 else "Deficit" for difvalm in dfdiff["Difference Medium"]]
    dfdiff["Low Deficit Or Surplus"] = ["Surplus" if difvall >= 0 else "Deficit" for difvall in dfdiff["Difference Low"]]

    bargraphc_high_px = px.bar(
        dfdiff,
        hover_data=["Year", "HighRevenue", "total_cost", "Difference High"],
        x="Year",
        y="Difference High",
        color="High Deficit Or Surplus",
        color_discrete_map={
            "Deficit": "#ac162c",
            "Surplus": "#001f5b"
        }
        # title="Revenue"
    )

    bargraphc_high_px.update_layout(
        yaxis=dict(title='Monetary Value (USD)'),
        xaxis=dict(title='Year'),
        legend=dict(title='Deficit or Surplus')
    )
    bargraphc_med_px = px.bar(
        dfdiff,
        hover_data=["Year", "MedRevenue", "total_cost", "Difference Medium"],
        x="Year",
        y="Difference Medium",
        color="Medium Deficit Or Surplus",
        color_discrete_map={
            "Deficit": "#ac162c",
            "Surplus": "#001f5b"
        }
        # title="Revenue"
    )

    bargraphc_med_px.update_layout(
        yaxis=dict(title='Monetary Value (USD)'),
        xaxis=dict(title='Year'),
        legend=dict(title='Deficit or Surplus')
    )
    bargraphc_low_px = px.bar(
        dfdiff,
        hover_data=["Year", "LowRevenue", "total_cost", "Difference Low"],
        x="Year",
        y="Difference Low",
        color="Low Deficit Or Surplus",
        color_discrete_map={
            "Deficit": "#ac162c",
            "Surplus": "#001f5b"
        }
        # title="Revenue"
    )

    bargraphc_low_px.update_layout(
        yaxis=dict(title='Monetary Value (USD)'),
        xaxis=dict(title='Year'),
        legend=dict(title='Deficit or Surplus')
    )

    bargraph_compare_high_plot = PlotlyView(bargraphc_high_px, height=height, width=width)
    bargraph_compare_med_plot = PlotlyView(bargraphc_med_px, height=height, width=width)
    bargraph_compare_low_plot = PlotlyView(bargraphc_low_px, height=height, width=width)

    context = {
        'bargraph_low_plot': bargraph_low_plot,
        'bargraph_med_plot': bargraph_med_plot,
        'bargraph_high_plot': bargraph_high_plot,
        'bargraph_compare_low_plot': bargraph_compare_low_plot,
        'bargraph_compare_med_plot': bargraph_compare_med_plot,
        'bargraph_compare_high_plot': bargraph_compare_high_plot,


        # 'can_add_projects': has_permission(request, 'add_projects')
    }

    session.close()
    return render(request, 'project_inventory/revenue_vs_requirements.html', context)

def admin(request):
    """
    Controller for the Plots Page.
    """

    # Get projects from database
    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()

    add_rev_button = Button(
        display_text='Add Revenues',
        name='add-button',
        icon='glyphicon glyphicon-plus',
        style='success',
        attributes={'onclick': 'importRevenueToDb();'},
        submit=True
    )

    add_proj_button = Button(
        display_text='Add Projects',
        name='add-button',
        icon='glyphicon glyphicon-plus',
        style='success',
        attributes={'onclick': 'importProjectsToDb();'},
        submit=True
    )


    context = {
        'add_rev_button':add_rev_button,
        'add_project_button': add_proj_button,
    }

    session.close()
    return render(request, 'project_inventory/admin.html', context)