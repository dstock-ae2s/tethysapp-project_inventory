from tethys_gizmos.gizmo_options import PlotlyView
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json
from .app import ProjectInventory as app
from .model import Project, Revenue


def create_capital_costs_bargraph(height='520 px', width='100%'):
    """
    Generates a plotly view of projects
    """
    # Get objects from database
    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()
    projects = session.query(Project).all()

    df = pd.DataFrame(columns=['Construction Year', 'Projected Cost', 'Facility ID', 'Project', 'Category'])

    for project in projects:

        if project.recur_checkbox_val == "true":
            y = 0
            for x in range(len(project.const_cost) - 1):
                df = df.append({'Construction Year': int(project.const_year) + y,
                                'Projected Cost': int(json.loads(project.const_cost[x + 1])),
                                'Facility ID': project.facility_id, 'Project': project.project,
                                'Category': project.category}, ignore_index=True)
                y = y + 1

        else:
            df = df.append(
                {'Construction Year': int(project.const_year), 'Projected Cost': int(json.loads(project.const_cost[0])),
                 'Facility ID': project.facility_id, 'Project': project.project, 'Category': project.category},
                ignore_index=True)

    # Build up Plotly plot
    bargraph_px = px.bar(
        df,
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
            "Storm": "#F78F07"}

        # colors="black"
        # name='Category',
        # title="Future Project Costs"
    )

    bargraph_px.update_layout(
        yaxis=dict(title='Construction Cost (USD)',),
        xaxis=dict(title='Construction Year'),
        legend=dict(title='Category')
    )


    bargraph_plot = PlotlyView(bargraph_px, height=height, width=width)
    session.close()
    return bargraph_plot

def create_capital_costs_piechart(height='520 px', width='100%'):
    """
    Generates a plotly view of projects
    """
    # Get objects from database
    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()
    projects = session.query(Project).all()

    df = pd.DataFrame(columns=['Construction Year', 'Projected Cost', 'Facility ID', 'Project', 'Category'])

    for project in projects:


        if project.recur_checkbox_val == "true":
            y = 0
            for x in range(len(project.const_cost) - 1):
                df = df.append({'Construction Year': int(project.const_year) + y,
                                'Projected Cost': int(json.loads(project.const_cost[x + 1])),
                                'Facility ID': project.facility_id, 'Project': project.project,
                                'Category': project.category}, ignore_index=True)
                y = y + 1

        else:
            df = df.append(
                {'Construction Year': int(project.const_year), 'Projected Cost': int(json.loads(project.const_cost[0])),
                 'Facility ID': project.facility_id, 'Project': project.project, 'Category': project.category},
                ignore_index=True)

    # Build up Plotly plot
    piechart_px = px.pie(
        df,
        values="Projected Cost",
        names="Category",
        labels="Category",
        color="Category",
        hover_data=["Category","Facility ID","Construction Year","Projected Cost"],
        color_discrete_map={
            "Water": "#056eb7",
            "Wastewater": "#b3c935",
            "Existing Debt": "#001f5b",
            "Facilities": "#074768",
            "Golf": "#ac162c",
            "Transportation": "#232525",
            "Storm": "#F78F07"}
    )

    piechart_plot = PlotlyView(piechart_px, height=height, width=width)
    session.close()
    return piechart_plot

def create_capital_costs_sunburst(height='520 px', width='100%'):
    """
    Generates a plotly view of projects
    """
    # Get objects from database
    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()
    projects = session.query(Project).all()

    df = pd.DataFrame(columns=['Construction Year', 'Projected Cost', 'Facility ID', 'Project', 'Category'])

    for project in projects:

        if project.recur_checkbox_val == "true":
            y = 0
            for x in range(len(project.const_cost)-1):

                df = df.append({'Construction Year': int(project.const_year) + y, 'Projected Cost': int(json.loads(project.const_cost[x + 1])), 'Facility ID': project.facility_id, 'Project': project.project, 'Category': project.category}, ignore_index=True)
                y = y+1

        else:
            df = df.append({'Construction Year': int(project.const_year), 'Projected Cost': int(json.loads(project.const_cost[0])), 'Facility ID': project.facility_id, 'Project': project.project, 'Category': project.category}, ignore_index=True)

    # Build up Plotly plot
    sunburst_px = px.sunburst(
        df,
        path=['Category', 'Facility ID','Project'],
        values='Projected Cost',
        color='Category',
        labels=df["Category"],
        color_discrete_map={
            "Water": "#056eb7",
            "Wastewater": "#b3c935",
            "Existing Debt": "#001f5b",
            "Facilities": "#074768",
            "Golf": "#ac162c",
            "Transportation": "#232525",
            "Storm": "#F78F07"}
        # text=df["Project"],
        # customdata=df["Construction Year"],
        # hovertemplate="Facility ID: %{label} <br>Project: %{path[2]} <br>Construction Year: %{customdata} <br>Cost: %{value}"

    )

    sunburst_plot = PlotlyView(sunburst_px, height=height, width=width)
    session.close()
    return sunburst_plot


def create_revenue_requirements_bargraph(height='520 px', width='100%'):
    """
    Generates a plotly view of projects
    """
    # Get objects from database
    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()
    projects = session.query(Project).all()

    df = pd.DataFrame(columns=['Construction Year', 'Projected Cost', 'Facility ID', 'Project', 'Category'])

    for project in projects:

        if project.debt_checkbox_val == "true":
            z =1
            for c in range(len(project.const_cost)-1):
                df = df.append({'Construction Year': int(project.const_year) + z, 'Projected Cost': int(json.loads(project.const_cost[c + 1])), 'Facility ID': project.facility_id, 'Project': project.project, 'Category': project.category}, ignore_index=True)
                z = z+1

        elif project.recur_checkbox_val == "true":
            y = 0
            for x in range(len(project.const_cost)-1):

                df = df.append({'Construction Year': int(project.const_year) + y, 'Projected Cost': int(json.loads(project.const_cost[x + 1])), 'Facility ID': project.facility_id, 'Project': project.project, 'Category': project.category}, ignore_index=True)
                y = y+1

        else:
            df = df.append({'Construction Year': int(project.const_year), 'Projected Cost': int(json.loads(project.const_cost[0])), 'Facility ID': project.facility_id, 'Project': project.project, 'Category': project.category}, ignore_index=True)


    # Build up Plotly plot
    bargraph_px = px.bar(
        df,
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
            "Storm": "#F78F07"}
        # title="Future Project Costs"
    )

    bargraph_px.update_layout(
        yaxis=dict(title='Revenue Required (USD)',),
        xaxis=dict(title='Year'),
        legend=dict(title='Category')
    )

    bargraph_plot = PlotlyView(bargraph_px, height=height, width=width)
    session.close()
    return bargraph_plot

def create_revenue_requirements_piechart(height='520 px', width='100%'):
    """
    Generates a plotly view of projects
    """
    # Get objects from database
    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()
    projects = session.query(Project).all()

    df = pd.DataFrame(columns=['Construction Year', 'Projected Cost', 'Facility ID', 'Project', 'Category'])

    for project in projects:
        if project.debt_checkbox_val == "true":
            z = 1
            for c in range(len(project.const_cost)-1):
                df = df.append({'Construction Year': int(project.const_year) + z, 'Projected Cost': int(json.loads(project.const_cost[c + 1])),
                                'Facility ID': project.facility_id, 'Project': project.project,
                                'Category': project.category}, ignore_index=True)
                z = z+1
        elif project.recur_checkbox_val == "true":
            y = 0
            for x in range(len(project.const_cost)-1):
                df = df.append({'Construction Year': int(project.const_year) + y, 'Projected Cost': int(json.loads(project.const_cost[x + 1])),
                                'Facility ID': project.facility_id, 'Project': project.project,
                                'Category': project.category}, ignore_index=True)
                y = y+1
        else:
            df = df.append({'Construction Year': int(project.const_year), 'Projected Cost': int(json.loads(project.const_cost[0])),
                            'Facility ID': project.facility_id, 'Project': project.project,
                            'Category': project.category}, ignore_index=True)

    # Build up Plotly plot
    piechart_px = px.pie(
        df,
        values="Projected Cost",
        labels="Category",
        names="Category",
        hover_data=["Facility ID","Project","Construction Year", "Projected Cost"],
        color="Category",
        color_discrete_map={
            "Water": "#056eb7",
            "Wastewater": "#b3c935",
            "Existing Debt": "#001f5b",
            "Facilities": "#074768",
            "Golf": "#ac162c",
            "Transportation": "#232525",
            "Storm": "#F78F07"}
    )

    piechart_plot = PlotlyView(piechart_px, height=height, width=width)
    session.close()
    return piechart_plot

def create_revenue_requirements_sunburst(height='520 px', width='100%'):
    """
    Generates a plotly view of projects
    """
    # Get objects from database
    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()
    projects = session.query(Project).all()

    df = pd.DataFrame(columns=['Construction Year', 'Projected Cost', 'Facility ID', 'Project', 'Category'])

    for project in projects:
        if project.debt_checkbox_val == "true":
            z = 1
            for c in range(len(project.const_cost)-1):
                df=df.append({'Construction Year': int(project.const_year) + z, 'Projected Cost': int(json.loads(project.const_cost[c + 1])), 'Facility ID': project.facility_id, 'Project':project.project, 'Category':project.category}, ignore_index=True)
                z=z+1
        elif project.recur_checkbox_val == "true":
            y=0
            for x in range(len(project.const_cost)-1):
                df = df.append({'Construction Year': int(project.const_year) + y, 'Projected Cost': int(json.loads(project.const_cost[x + 1])), 'Facility ID': project.facility_id, 'Project': project.project, 'Category': project.category}, ignore_index=True)
                y=y+1
        else:
            df = df.append({'Construction Year': int(project.const_year), 'Projected Cost': int(json.loads(project.const_cost[0])), 'Facility ID': project.facility_id, 'Project': project.project, 'Category': project.category}, ignore_index=True)

    # Build up Plotly plot
    sunburst_px = px.sunburst(
        df,
        path=['Category', 'Facility ID','Project'],
        values='Projected Cost',
        color='Category',
        labels=df["Category"],
        # text=df["Project"],
        # customdata=df["Construction Year"],
        # hovertemplate="Facility ID: %{label} <br>Project: %{path[2]} <br>Construction Year: %{customdata} <br>Cost: %{value}"

    )

    sunburst_plot = PlotlyView(sunburst_px, height=height, width=width)
    session.close()
    return sunburst_plot



def create_revenue_bargraph(rev_scenario):
    height = '520px'
    width = '100%'

    """
    Generates a plotly view of projects
    """

    # Get objects from database
    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()
    revenue_list = session.query(Revenue).all()


    df = pd.DataFrame(columns=['Scenario', 'Source', 'Monetary Value', 'Year'])



    for entry in revenue_list:

        if entry.scenario == rev_scenario:

            df = df.append({'Scenario': entry.scenario, 'Source': entry.revenue_source, 'Monetary Value': int(json.loads(entry.monetary_Value)), 'Year': entry.year}, ignore_index=True)


    # Build up Plotly plot
    bargraph_px = px.bar(
        df,
        hover_data=["Source", "Monetary Value", "Year"],
        x="Year",
        y="Monetary Value",
        color="Source"
        # title="Revenue"
    )

    bargraph_px.update_layout(
        yaxis=dict(title='Revenue (USD)'),
        xaxis=dict(title='Year'),
        legend=dict(title='Source of Revenue')
    )


    bargraph_plot = PlotlyView(bargraph_px, height=height, width=width)

    session.close()
    return bargraph_plot

def create_revenue_piechart(rev_scenario):
    height = '520px'
    width = '100%'
    """
    Generates a plotly view of projects
    """
    # Get objects from database
    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()
    revenue_list = session.query(Revenue).all()

    df = pd.DataFrame(columns=['Scenario', 'Source', 'Monetary Value', 'Year'])

    for entry in revenue_list:

        if entry.scenario == rev_scenario:

            df = df.append({'Scenario': entry.scenario, 'Source': entry.revenue_source,
                            'Monetary Value': int(json.loads(entry.monetary_Value)), 'Year': entry.year},
                           ignore_index=True)

    # Build up Plotly plot
    piechart_go = go.Figure(go.Pie(
        name="",
        values=df["Monetary Value"],
        labels=df["Source"],
        text=df["Source"],
        customdata=df["Year"],
        hovertemplate="Source: %{label} <br> Scenario: %{text} <br> Year: %{customdata} <br>Revenue: %{value}"
    ))

    piechart_plot = PlotlyView(piechart_go, divid="pie-plot-rev-div", height=height, width=width)
    session.close()
    return piechart_plot



def create_revenue_sunburst(height='520 px', width='100%'):
    """
    Generates a plotly view of projects
    """
    # Get objects from database
    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()
    revenue_list = session.query(Revenue).all()

    dfhigh = pd.DataFrame(columns=['Scenario', 'Source', 'Monetary Value', 'Year'])
    dfmed = pd.DataFrame(columns=['Scenario', 'Source', 'Monetary Value', 'Year'])
    dflow = pd.DataFrame(columns=['Scenario', 'Source', 'Monetary Value', 'Year'])

    for entry in revenue_list:

        if entry.scenario == "high":

            dfhigh = dfhigh.append({'Scenario': entry.scenario, 'Source': entry.revenue_source,
                                    'Monetary Value': int(json.loads(entry.monetary_Value)), 'Year': entry.year},
                                   ignore_index=True)

        elif entry.scenario == "medium":
            dfmed = dfmed.append({'Scenario': entry.scenario, 'Source': entry.revenue_source,
                                  'Monetary Value': int(json.loads(entry.monetary_Value)), 'Year': entry.year},
                                 ignore_index=True)


        elif entry.scenario == "low":

            dflow = dflow.append({'Scenario': entry.scenario, 'Source': entry.revenue_source,
                                  'Monetary Value': int(json.loads(entry.monetary_Value)), 'Year': entry.year},
                                 ignore_index=True)
    # Build up Plotly plot
    sunburst_px = px.sunburst(
        dfmed,
        path=['Source', 'Year','Monetary Value'],
        values='Monetary Value',
        color='Source',
        labels=dfmed["Source"],
        # text=df["Project"],
        # customdata=df["Construction Year"],
        # hovertemplate="Facility ID: %{label} <br>Project: %{path[2]} <br>Construction Year: %{customdata} <br>Cost: %{value}"

    )

    sunburst_plot = PlotlyView(sunburst_px, divid="sun-plot-rev-div",height=height, width=width)
    session.close()
    return sunburst_plot


def create_revenue_vs_requirements_bargraph(rev_scenario):
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
            z =1
            for c in range(len(project.const_cost)-1):
                dfrevreq = dfrevreq.append({'Construction Year': int(project.const_year) + z, 'Projected Cost': float(json.loads(project.const_cost[c + 1])), 'Facility ID': project.facility_id, 'Project': project.project, 'Category': project.category}, ignore_index=True)
                z = z+1
        elif project.recur_checkbox_val == "true":
            y = 0
            for x in range(len(project.const_cost)-1):

                dfrevreq = dfrevreq.append({'Construction Year': int(project.const_year) + y, 'Projected Cost': float(json.loads(project.const_cost[x + 1])), 'Facility ID': project.facility_id, 'Project': project.project, 'Category': project.category}, ignore_index=True)
                y = y+1
        else:
            dfrevreq = dfrevreq.append({'Construction Year': int(project.const_year), 'Projected Cost': float(json.loads(project.const_cost[0])), 'Facility ID': project.facility_id, 'Project': project.project, 'Category': project.category}, ignore_index=True)

    print("bargraph data ready")
    # Build up Plotly plot
    bargraph_px = px.bar(
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
            "Storm": "#F78F07"}
        # title="Future Project Costs"
    )

    bargraph_px.update_layout(
        yaxis=dict(title='Construction Cost (USD)',),
        xaxis=dict(title='Construction Year'),
        legend=dict(title='Category')
    )
    print("bargraphdone")

    dfrev = pd.DataFrame(columns=['Scenario', 'Source', 'Monetary Value', 'Year'])



    for entry in revenue_list:

        if entry.scenario == rev_scenario:

            dfrev = dfrev.append({'Scenario': entry.scenario, 'Source': entry.revenue_source, 'Monetary Value': int(json.loads(entry.monetary_Value)), 'Year': int(entry.year)}, ignore_index=True)

    print("rev done")
    dfrev_sum = dfrev.groupby("Year").agg(Revenue=('Monetary Value','sum'))
    dfrevfinal = pd.DataFrame(columns=["Year"])

    minyr = dfrev["Year"].min()
    maxyr = dfrev["Year"].max()

    year_range = []

    for i in range(maxyr - minyr + 1):
        year_range.append(minyr + i)

    for year in year_range:
        dfrevfinal = dfrevfinal.append({'Year': year}, ignore_index=True)

    dfrevfinal = dfrevfinal.merge(dfrev_sum, how="left", on="Year")

    print("groupby done")
    bargraph_px.add_scatter(y=dfrevfinal["Revenue"], x=dfrevfinal["Year"], mode="lines",
                    line=dict(width=3,color="Red"),
                    name=rev_scenario)


    print("scatter done")
    bargraph_plot = PlotlyView(bargraph_px, height=height, width=width)
    print("graph generated")
    session.close()
    return bargraph_plot

def create_revenue_vs_requirements_piechart(height='520 px', width='100%'):
    """
    Generates a plotly view of projects
    """
    # Get objects from database
    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()
    projects = session.query(Project).all()

    dfrevreq = pd.DataFrame(columns=['Construction Year', 'Projected Cost', 'Facility ID', 'Project', 'Category'])

    for project in projects:

        if project.debt_checkbox_val == "true":
            z = 1
            for c in range(len(project.const_cost) - 1):
                dfrevreq = dfrevreq.append({'Construction Year': int(project.const_year) + z,
                                            'Projected Cost': int(json.loads(project.const_cost[c + 1])),
                                            'Facility ID': project.facility_id, 'Project': project.project,
                                            'Category': project.category}, ignore_index=True)
                z = z + 1
        elif project.recur_checkbox_val == "true":
            y = 0
            for x in range(len(project.const_cost) - 1):
                dfrevreq = dfrevreq.append({'Construction Year': int(project.const_year) + y,
                                            'Projected Cost': int(json.loads(project.const_cost[x + 1])),
                                            'Facility ID': project.facility_id, 'Project': project.project,
                                            'Category': project.category}, ignore_index=True)
                y = y + 1
        else:
            dfrevreq = dfrevreq.append(
                {'Construction Year': int(project.const_year), 'Projected Cost': int(json.loads(project.const_cost[0])),
                 'Facility ID': project.facility_id, 'Project': project.project, 'Category': project.category},
                ignore_index=True)
    print("cost data ready")
    # Build up Plotly plot
    piechart_px = px.pie(
        df,
        values="Projected Cost",
        labels="Category",
        names="Category",
        hovertemplate=["Facility ID", "Project", "Construction Year", "Cost"],
        color="Category",
        color_discrete_map={
            "Water": "#056eb7",
            "Wastewater": "#b3c935",
            "Existing Debt": "#001f5b",
            "Facilities": "#074768",
            "Golf": "#ac162c",
            "Transportation": "#232525",
            "Storm": "#F78F07"}
    )
    print("piechart done")
    piechart_plot = PlotlyView(piechart_px, height=height, width=width)
    print("Plot rendered")
    session.close()
    return piechart_plot

def create_revenue_vs_requirements_sunburst(height='520 px', width='100%'):
    """
    Generates a plotly view of projects
    """
    # Get objects from database
    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()
    projects = session.query(Project).all()

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
            dfrevreq = dfrevreq.append(
                {'Construction Year': int(project.const_year), 'Projected Cost': float(json.loads(project.const_cost[0])),
                 'Facility ID': project.facility_id, 'Project': project.project, 'Category': project.category},
                ignore_index=True)



    # Build up Plotly plot
    sunburst_px = px.sunburst(
        dfrevreq,
        path=['Category', 'Facility ID','Project'],
        values='Projected Cost',
        color='Category',
        labels=dfrevreq["Category"],
        # text=df["Project"],
        # customdata=df["Construction Year"],
        # hovertemplate="Facility ID: %{label} <br>Project: %{path[2]} <br>Construction Year: %{customdata} <br>Cost: %{value}"

    )

    sunburst_plot = PlotlyView(sunburst_px, height=height, width=width)
    session.close()
    return sunburst_plot


def create_revenue_vs_req_compare_bargraph(rev_scenario):
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

    dfrevreq = pd.DataFrame(columns=['Construction Year', 'Projected Cost',])
    print("difference data started")
    for project in projects:

        if project.debt_checkbox_val == "true":
            z = 1
            for c in range(len(project.const_cost) - 1):
                dfrevreq = dfrevreq.append({'Construction Year': int(project.const_year) + z,
                                            'Projected Cost': float(json.loads(project.const_cost[c + 1]))
                                            }, ignore_index=True)
                z = z + 1
        elif project.recur_checkbox_val == "true":
            y = 0
            for x in range(len(project.const_cost) - 1):
                dfrevreq = dfrevreq.append({'Construction Year': int(project.const_year) + y,
                                            'Projected Cost': float(json.loads(project.const_cost[x + 1])),
                                            }, ignore_index=True)
                y = y + 1
        else:
            dfrevreq = dfrevreq.append(
                {'Construction Year': int(project.const_year), 'Projected Cost': float(json.loads(project.const_cost[0])),
                 'Facility ID': project.facility_id, 'Project': project.project, 'Category': project.category},
                ignore_index=True)

    dfrev = pd.DataFrame(columns=['Scenario', 'Source', 'Monetary Value', 'Year'])



    for entry in revenue_list:

        if entry.scenario == rev_scenario:

            dfrev = dfrev.append({'Scenario': entry.scenario, 'Source': entry.revenue_source, 'Monetary Value': float(json.loads(entry.monetary_Value)), 'Year': int(entry.year)}, ignore_index=True)

    dfrevreq_rnm = dfrevreq.rename(columns={"Construction Year": "Year"})

    dfrev_sum = dfrev.groupby("Year").agg(total_rev=('Monetary Value', 'sum'))

    dfrevreq_sum = dfrevreq_rnm.groupby("Year").agg(total_cost=('Projected Cost', 'sum'))

    minyr = min(int(dfrevreq_rnm["Year"].min()), int(dfrev["Year"].min()))
    maxyr = max(int(dfrevreq_rnm["Year"].max()), int(dfrev["Year"].max()))

    year_range = []

    for i in range(maxyr - minyr + 1):
        year_range.append(minyr+i)
    dfdiff = pd.DataFrame(columns = ["Year", "Difference"])
    for year in year_range:

        dfdiff=dfdiff.append({'Year': year, "Difference":0}, ignore_index=True)


    dfdiff = dfdiff.merge(dfrev_sum, how="left", on="Year")
    dfdiff = dfdiff.merge(dfrevreq_sum, how="left", on="Year")

    dfdiff["total_rev"]=dfdiff["total_rev"].fillna(0)
    dfdiff["total_cost"] = dfdiff["total_cost"].fillna(0)
    dfdiff["Difference"] = (dfdiff["total_rev"] - dfdiff["total_cost"])

    dfdiff["Loss Or Gain"] = ["Gain" if difval >=0 else "Loss" for difval in dfdiff["Difference"]]

    print("difference data finished")


    # Build up Plotly plot
    bargraph_px = px.bar(
        dfdiff,
        hover_data=["Year", "total_rev", "total_cost", "Difference"],
        x="Year",
        y="Difference",
        color="Loss Or Gain",
        color_discrete_map={
            "Loss":"#ac162c",
            "Gain":"#001f5b"
        }
        # title="Revenue"
    )

    bargraph_px.update_layout(
        yaxis=dict(title='Revenue (USD)'),
        xaxis=dict(title='Year'),
        legend=dict(title='Source of Revenue')
    )


    bargraph_plot = PlotlyView(bargraph_px, height=height, width=width)

    session.close()
    return bargraph_plot


def create_revenue_vs_requirements_graphs():
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
            z =1
            for c in range(len(project.const_cost)-1):
                dfrevreq = dfrevreq.append({'Construction Year': int(project.const_year) + z, 'Projected Cost': float(json.loads(project.const_cost[c + 1])), 'Facility ID': project.facility_id, 'Project': project.project, 'Category': project.category}, ignore_index=True)
                z = z+1
        elif project.recur_checkbox_val == "true":
            y = 0
            for x in range(len(project.const_cost)-1):

                dfrevreq = dfrevreq.append({'Construction Year': int(project.const_year) + y, 'Projected Cost': float(json.loads(project.const_cost[x + 1])), 'Facility ID': project.facility_id, 'Project': project.project, 'Category': project.category}, ignore_index=True)
                y = y+1
        else:
            dfrevreq = dfrevreq.append({'Construction Year': int(project.const_year), 'Projected Cost': float(json.loads(project.const_cost[0])), 'Facility ID': project.facility_id, 'Project': project.project, 'Category': project.category}, ignore_index=True)

    print("bargraph data ready")
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
            "Existing Debt": "#001f5b",
            "Facilities": "#074768",
            "Golf": "#ac162c",
            "Transportation": "#232525",
            "Storm": "#F78F07"}
        # title="Future Project Costs"
    )

    bargraph_high_px.update_layout(
        yaxis=dict(title='Construction Cost (USD)',),
        xaxis=dict(title='Construction Year'),
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
            "Storm": "#F78F07"}
        # title="Future Project Costs"
    )

    bargraph_med_px.update_layout(
        yaxis=dict(title='Construction Cost (USD)', ),
        xaxis=dict(title='Construction Year'),
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
            "Storm": "#F78F07"}
        # title="Future Project Costs"
    )

    bargraph_low_px.update_layout(
        yaxis=dict(title='Construction Cost (USD)', ),
        xaxis=dict(title='Construction Year'),
        legend=dict(title='Category')
    )
    print("bargraphdone")

    dfrevhigh = pd.DataFrame(columns=['Scenario', 'Source', 'Monetary Value', 'Year'])
    dfrevmed = pd.DataFrame(columns=['Scenario', 'Source', 'Monetary Value', 'Year'])
    dfrevlow = pd.DataFrame(columns=['Scenario', 'Source', 'Monetary Value', 'Year'])




    for entry in revenue_list:

        if entry.scenario == "high":

            dfrevhigh = dfrevhigh.append({'Scenario': entry.scenario, 'Source': entry.revenue_source, 'Monetary Value': int(json.loads(entry.monetary_Value)), 'Year': int(entry.year)}, ignore_index=True)
        elif entry.scenario == "medium":

            dfrevmed = dfrevmed.append({'Scenario': entry.scenario, 'Source': entry.revenue_source, 'Monetary Value': int(json.loads(entry.monetary_Value)), 'Year': int(entry.year)}, ignore_index=True)
        elif entry.scenario == "low":

            dfrevlow = dfrevlow.append({'Scenario': entry.scenario, 'Source': entry.revenue_source, 'Monetary Value': int(json.loads(entry.monetary_Value)), 'Year': int(entry.year)}, ignore_index=True)



    dfrevhigh_sum = dfrevhigh.groupby("Year").agg(HigRevenue=('Monetary Value','sum'))
    dfrevmed_sum = dfrevmed.groupby("Year").agg(MedRevenue=('Monetary Value','sum'))
    dfrevlow_sum = dfrevlow.groupby("Year").agg(LowRevenue=('Monetary Value','sum'))

    dfrevfinal = pd.DataFrame(columns=["Year"])

    minyr = dfrev["Year"].min()
    maxyr = dfrev["Year"].max()

    year_range = []

    for i in range(maxyr - minyr + 1):
        year_range.append(minyr + i)

    for year in year_range:
        dfrevfinal = dfrevfinal.append({'Year': year}, ignore_index=True)

    dfrevfinal = dfrevfinal.merge(dfrevlow_sum, how="left", on="Year")
    dfrevfinal = dfrevfinal.merge(dfrevmed_sum, how="left", on="Year")
    dfrevfinal = dfrevfinal.merge(dfrevhigh_sum, how="left", on="Year")


    print("groupby done")
    bargraph_high_px.add_scatter(y=dfrevfinal["HighRevenue"], x=dfrevfinal["Year"], mode="lines",
                    line=dict(width=3,color="Red"),
                    name="High Revenue Scenario")
    bargraph_med_px.add_scatter(y=dfrevfinal["MedRevenue"], x=dfrevfinal["Year"], mode="lines",
                                 line=dict(width=3, color="Red"),
                                 name="High Revenue Scenario")
    bargraph_low_px.add_scatter(y=dfrevfinal["LowRevenue"], x=dfrevfinal["Year"], mode="lines",
                                 line=dict(width=3, color="Red"),
                                 name="High Revenue Scenario")


    print("scatter done")
    bargraph_high_plot = PlotlyView(bargraph_high_px, height=height, width=width)
    bargraph_med_plot = PlotlyView(bargraph_med_px, height=height, width=width)
    bargraph_low_plot = PlotlyView(bargraph_low_px, height=height, width=width)
    print("graph generated")
    session.close()
    return (bargraph_high_plot, bargraph_med_plot, bargraph_low_plot)