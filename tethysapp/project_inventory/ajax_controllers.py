from .model import Project, add_new_project, get_all_projects
from django.http import JsonResponse, HttpResponse, Http404
from .app import ProjectInventory as app
import json

def get_project_list (request):
    if request.is_ajax() and request.method == 'POST':
        fac_id = request.POST['facility_id']

        project_list = get_all_projects()

        return_obj = {}
        fac_projname_list = []
        fac_projcost_list = []
        fac_projyear_list = []
        fac_projcategory_list = []
        fac_projdescription_list = []
        fac_projpriority_list = []
        fac_projestyear_list = []
        fac_projconstcost_list = []


        for project in project_list:
            if project.facility_id == fac_id:
                fac_projname_list.append(project.project)
                fac_projcost_list.append(project.cost)
                fac_projyear_list.append(project.planned_year)
                fac_projcategory_list.append(project.category)
                fac_projdescription_list.append(project.description)
                fac_projpriority_list.append(project.priority)
                fac_projestyear_list.append(project.est_year)
                fac_projconstcost_list.append(project.const_cost)

        return_obj["project_name"] = fac_projname_list
        return_obj["cost"] = fac_projcost_list
        return_obj["planned_year"] = fac_projyear_list
        return_obj["category"] = fac_projcategory_list
        return_obj["description"] = fac_projdescription_list
        return_obj["priority"] = fac_projpriority_list
        return_obj["est_year"] = fac_projestyear_list
        return_obj["const_cost"] = fac_projconstcost_list

        print("GET PROJECT LIST AJAX")
        print(return_obj)

        return JsonResponse(return_obj)


def save_updates_to_db (request):
    return_obj = {}
    if request.is_ajax() and request.method == 'POST':
        fac_id = request.POST['facility_id']
        project_name_string = request.POST['project_name_list']
        project_name_list = json.loads(project_name_string)
        project_cost_list = json.loads(request.POST['project_cost_list'])
        project_year_list = json.loads(request.POST['project_year_list'])
        project_category_list = json.loads(request.POST['project_category_list'])
        project_description_list = json.loads(request.POST['project_description_list'])
        project_priority_list = json.loads(request.POST['project_priority_list'])
        project_est_year = json.loads(request.POST['project_est_year_list'])
        project_const_cost_list = json.loads(request.POST['project_const_cost_list'])

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
            # Create new Project record
            new_project = Project(
             latitude=latitude,
             longitude=longitude,
             facility_id=fac_id,
             project=project_name_list[i],
             cost=project_cost_list[i],
             planned_year=project_year_list[i],
             category=project_category_list[i],
             description=project_description_list[i],
             priority=project_priority_list[i],
             est_year=project_est_year,
             const_cost=project_const_cost_list[i],
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