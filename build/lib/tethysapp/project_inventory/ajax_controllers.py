from .model import Project, add_new_project, get_all_projects, add_new_revenue, get_all_revenue,add_new_project_from_csv
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import render, reverse, redirect
from .app import ProjectInventory as app
from .helpers import *
import json
import csv

def get_project_list (request):
    if request.is_ajax() and request.method == 'POST':
        fac_id = request.POST['facility_id']

        project_list = get_all_projects()

        return_obj = {}
        fac_projname_list = []
        fac_projestcost_list = []
        fac_projconstyear_list = []
        fac_projcategory_list = []
        fac_projdescription_list = []
        fac_projpriority_list = []
        fac_projestyear_list = []
        fac_projconstcost_list = []
        fac_debt_checkbox_list = []
        fac_recur_checkbox_list = []


        for project in project_list:
            if project.facility_id == fac_id:
                fac_projname_list.append(project.project)
                fac_projestcost_list.append(project.est_cost)
                fac_projconstyear_list.append(project.const_year)
                fac_projcategory_list.append(project.category)
                fac_projdescription_list.append(project.description)
                fac_projpriority_list.append(project.priority)
                fac_projestyear_list.append(project.est_year)
                fac_projconstcost_list.append(project.const_cost[0])
                fac_debt_checkbox_list.append(project.debt_checkbox_val)
                fac_recur_checkbox_list.append(project.recur_checkbox_val)

        return_obj["project_name"] = fac_projname_list
        return_obj["est_cost"] = fac_projestcost_list
        return_obj["const_year"] = fac_projconstyear_list
        return_obj["category"] = fac_projcategory_list
        return_obj["description"] = fac_projdescription_list
        return_obj["priority"] = fac_projpriority_list
        return_obj["est_year"] = fac_projestyear_list
        return_obj["const_cost"] = fac_projconstcost_list
        return_obj["debt_checkbox"] = fac_debt_checkbox_list
        return_obj["recur_checkbox"] = fac_recur_checkbox_list

        print("GET PROJECT LIST AJAX")
        print(return_obj)

        return JsonResponse(return_obj)


def save_updates_to_db (request):
    return_obj = {}
    if request.is_ajax() and request.method == 'POST':
        interest_rate = 0.04
        inflation_rate = 0.04
        recur_years = 20
        pay_period = 20
        fac_id = request.POST['facility_id']
        project_name_string = request.POST['project_name_list']
        project_name_list = json.loads(project_name_string)
        project_est_cost_list = json.loads(request.POST['project_est_cost_list'])
        project_const_year_list = json.loads(request.POST['project_const_year_list'])
        project_category_list = json.loads(request.POST['project_category_list'])
        project_description_list = json.loads(request.POST['project_description_list'])
        project_priority_list = json.loads(request.POST['project_priority_list'])
        project_est_year_list = json.loads(request.POST['project_est_year_list'])
        project_const_cost_list = json.loads(request.POST['project_const_cost_list'])
        debt_checkbox_list = json.loads(request.POST['debt_checkbox_list'])
        recur_checkbox_list = json.loads(request.POST['recur_checkbox_list'])


        print(project_est_cost_list)
        # Get connection/session to database
        Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
        session = Session()

        project_list = get_all_projects()
        for project in project_list:
            if project.facility_id == fac_id:
                latitude = project.latitude
                longitude = project.longitude
                session.delete(project)

        for i in range(len(project_name_list)):
            cost_array = []

            cost_array.append(project_const_cost_list[i])
            if debt_checkbox_list[i] == True:

                annual_payment = float(project_const_cost_list[i]) * (
                        (interest_rate * (1 + interest_rate) ** (pay_period)) / (
                            (1 + interest_rate) ** (pay_period) - 1))
                for _ in range(pay_period-1):
                    cost_array.append(round(annual_payment))
                    print(annual_payment)

            elif recur_checkbox_list[i] == True:
                annual_payment = float(project_const_cost_list[i])
                for j in range(recur_years):
                    annual_payment = annual_payment * ((inflation_rate+1))
                    cost_array.append(round(annual_payment))
                    print(annual_payment)

            print(project_est_cost_list[i])
            # Create new Project record
            new_project = Project(
                latitude=latitude,
                longitude=longitude,
                facility_id=fac_id,
                project=project_name_list[i],
                est_cost=project_est_cost_list[i],
                const_year=project_const_year_list[i],
                category=project_category_list[i],
                description=project_description_list[i],
                priority=project_priority_list[i],
                est_year=project_est_year_list[i],
                const_cost=cost_array,
                debt_checkbox_val=debt_checkbox_list[i],
                recur_checkbox_val=recur_checkbox_list[i],
            )
            session.add(new_project)

        # Commit the session and close the connection
        session.commit()
        session.close()


            # num_existing_projects = fac_projname_list.len

# # for each project in ajax project list, check if name is in db fac_projname_list.  if not add new db entry otherwise update existing entry
#         for proj in fac_projname_list:
#             if proj in fac_projname_list:
#                 #add new entry with coordinates
#             else:
#                 #update existing entry
#
#         return_obj["project_name"] = fac_projname_list
#         return_obj["cost"] = fac_projcost_list
#         return_obj["planned_year"] = fac_projyear_list

        return JsonResponse(return_obj)


def get_project_categorized_list (request):
    if request.is_ajax() and request.method == 'POST':
        category = request.POST['category']

        # Get connection/session to database
        Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
        session = Session()

        # Query for all project records
        project_list = session.query(Project).filter_by(category=category).all()
        session.close()

        return_obj = {}
        fac_projfacilityid_list = []
        fac_projname_list = []
        fac_projestcost_list = []
        fac_projconstyear_list = []
        fac_projdescription_list = []
        fac_projpriority_list = []
        fac_projestyear_list = []
        fac_projconstcost_list = []
        fac_debt_checkbox_list = []
        fac_recur_checkbox_list = []


        for project in project_list:
            fac_projfacilityid_list.append(project.facility_id)
            fac_projname_list.append(project.project)
            fac_projestcost_list.append(project.est_cost)
            fac_projconstyear_list.append(project.const_year)
            fac_projdescription_list.append(project.description)
            fac_projpriority_list.append(project.priority)
            fac_projestyear_list.append(project.est_year)
            fac_projconstcost_list.append(project.const_cost[0])
            fac_debt_checkbox_list.append(project.debt_checkbox_val)
            fac_recur_checkbox_list.append(project.recur_checkbox_val)

        return_obj["facility_id"] = fac_projfacilityid_list
        return_obj["project_name"] = fac_projname_list
        return_obj["est_cost"] = fac_projestcost_list
        return_obj["const_year"] = fac_projconstyear_list
        return_obj["description"] = fac_projdescription_list
        return_obj["priority"] = fac_projpriority_list
        return_obj["est_year"] = fac_projestyear_list
        return_obj["const_cost"] = fac_projconstcost_list
        return_obj["debt_checkbox"] = fac_debt_checkbox_list
        return_obj["recur_checkbox"] = fac_recur_checkbox_list

        print("GET PROJECT LIST AJAX")
        print(return_obj)

        return JsonResponse(return_obj)



def save_cat_updates_to_db (request):
    return_obj = {}
    if request.is_ajax() and request.method == 'POST':
        interest_rate = 0.04
        inflation_rate = 0.04
        recur_years = 20
        pay_period = 20
        category = request.POST['category']
        project_name_string = request.POST['project_name_list']
        project_name_list = json.loads(project_name_string)
        project_est_cost_list = json.loads(request.POST['project_est_cost_list'])
        project_const_year_list = json.loads(request.POST['project_const_year_list'])
        project_facility_id_list = json.loads(request.POST['project_facility_id_list'])
        project_description_list = json.loads(request.POST['project_description_list'])
        project_priority_list = json.loads(request.POST['project_priority_list'])
        project_est_year_list = json.loads(request.POST['project_est_year_list'])
        project_const_cost_list = json.loads(request.POST['project_const_cost_list'])
        debt_checkbox_list = json.loads(request.POST['debt_checkbox_list'])
        recur_checkbox_list = json.loads(request.POST['recur_checkbox_list'])


        print(project_est_cost_list)
        # Get connection/session to database
        Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
        session = Session()
        db_id = 1
        project_list = get_all_projects()
        for project in project_list:
            db_id = db_id+1
            if project.category == category:
                latitude = project.latitude
                longitude = project.longitude
                session.delete(project)

        for i in range(len(project_name_list)):
            cost_array = []

            cost_array.append(project_const_cost_list[i])
            if debt_checkbox_list[i] == True:

                annual_payment = float(project_const_cost_list[i]) * (
                        (interest_rate * (1 + interest_rate) ** (pay_period)) / (
                            (1 + interest_rate) ** (pay_period) - 1))
                for _ in range(pay_period-1):
                    cost_array.append(round(annual_payment))
                    print(annual_payment)

            elif recur_checkbox_list[i] == True:
                annual_payment = float(project_const_cost_list[i])
                for j in range(recur_years):
                    annual_payment = annual_payment * ((inflation_rate+1)**j)
                    cost_array.append(round(annual_payment))
                    print(annual_payment)

            print(project_est_cost_list[i])
            # Create new Project record
            new_project = Project(
                id=db_id+1,
                latitude=latitude,
                longitude=longitude,
                facility_id=project_facility_id_list[i],
                project=project_name_list[i],
                est_cost=project_est_cost_list[i],
                const_year=project_const_year_list[i],
                category=category,
                description=project_description_list[i],
                priority=project_priority_list[i],
                est_year=project_est_year_list[i],
                const_cost=cost_array,
                debt_checkbox_val=debt_checkbox_list[i],
                recur_checkbox_val=recur_checkbox_list[i],
            )
            session.add(new_project)

        # Commit the session and close the connection
        session.commit()
        session.close()
        return JsonResponse(return_obj)

def import_revenue_to_db(request):
    return_obj ={}
    if request.is_ajax() and request.method == 'POST':

        Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
        session = Session()

        revenue_list = session.query(Revenue).all()
        row_id = len(revenue_list) +1

        with open('/Users/tmcstraw/Downloads/Revenue.csv', newline='') as f:
            reader = csv.reader(f)
            data = list(reader)

        print(data[0])
        print(data[1])
        print(len(data))

        for row in data:

                print(row[0])
                clean_val = ((row[1].replace("$","")).replace(",",""))
                print(row[2])
                print(row[3])

                add_new_revenue(row_id, row[3],row[2],clean_val,row[0])
                row_id = row_id +1

        session.close()
        return_obj['success'] = "success"

        return JsonResponse(return_obj)

def import_projects_to_db(request):
    return_obj ={}
    if request.is_ajax() and request.method == 'POST':

        Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
        session = Session()

        project_list = session.query(Project).all()
        row_id = len(project_list) +1

        with open('/Users/tmcstraw/Downloads/Costs.csv', newline='') as f:
            reader = csv.reader(f)
            data = list(reader)

        newdata = (data[1:])
        print(newdata)
        for row in newdata:
            print(row)

            latitude = row[0]
            longitude= row[1]
            facility_id = row[2]
            category = row[3]
            project = row[4]
            description = row[5]
            priority = row[6]
            est_cost = ((row[7].replace("$", "")).replace(",", ""))
            est_year = row[8]
            const_year = row[9]
            const_cost = ((row[10].replace("$", "")).replace(",", ""))
            debt_checkbox_val = row[12]
            recur_checkbox_val = row[13]






            add_new_project_from_csv(row_id, latitude, longitude, facility_id, project, est_cost, const_year, category, description, priority, est_year, const_cost, debt_checkbox_val, recur_checkbox_val)

            row_id = row_id +1

        session.close()
        return_obj['success'] = "success"

        return JsonResponse(return_obj)


# def reload_plotly_graphs(request):
#     return_obj = {}
#     if request.is_ajax() and request.method == 'POST':
#         rev_scenario = request.POST['rev_scenario']
#         start_date = request.POST['rev_scenario']
#         end_date = request.POST['rev_scenario']
#
#         bargraph_plot = create_revenue_bargraph(rev_scenario)
#
#         piechart_plot = create_revenue_vs_requirements_piechart()
#         sunburst_plot = create_revenue_vs_requirements_sunburst()
#
#         context = {
#             'bargraph_plot': bargraph_plot,
#             'piechart_plot': piechart_plot,
#             'sunburst_plot': sunburst_plot,
#             # 'can_add_projects': has_permission(request, 'add_projects')
#         }
#
#         return render(request,'project_inventory/revenue_vs_requirements.html', context)
#
#





