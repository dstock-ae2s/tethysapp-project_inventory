import json
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, ForeignKey, ARRAY
from sqlalchemy.orm import sessionmaker, relationship

from .app import ProjectInventory as app

Base = declarative_base()


# SQLAlchemy ORM definition for the projects table
class Revenue(Base):
    """
    SQLAlchemy Project DB Model
    """
    __tablename__ = 'revenue'

    # Columns
    id = Column(Integer, primary_key=True)
    scenario = Column(String)
    revenue_source = Column(String)
    monetary_Value = Column(String)
    year = Column(String)

class Project(Base):
    """
    SQLAlchemy Project DB Model
    """
    __tablename__ = 'projects'

    # Columns
    id = Column(Integer, primary_key=True)
    latitude = Column(Float)
    longitude = Column(Float)
    facility_id = Column(String)
    project = Column(String)
    est_year = Column(String)
    est_cost = Column(String)
    category = Column(String)
    description = Column(String)
    priority = Column(String)
    const_year = Column(String)
    const_cost = Column(ARRAY(String))
    debt_checkbox_val = Column(String)
    recur_checkbox_val = Column(String)


def add_new_project(row_id, location, facility_id, project, est_cost, const_year, category, description, priority, est_year, const_cost, debt_checkbox_val, recur_checkbox_val):
    """
    Persist new project.
    """
    # Convert GeoJSON to Python dictionary
    location_dict = json.loads(location)
    location_geometry = location_dict['geometries'][0]
    longitude = location_geometry['coordinates'][0]
    latitude = location_geometry['coordinates'][1]

    inflation_rate = 0.04
    interest_rate = 0.04
    pay_period = 20
    recur_years = 20

    cost_array = []
    cost_array.append(const_cost)
    print(debt_checkbox_val)
    if debt_checkbox_val == "true":
        annual_payment = float(const_cost) * (
                (interest_rate * (1 + interest_rate) ** (pay_period)) / (
                (1 + interest_rate) ** (pay_period) - 1))
        for _ in range(pay_period-1):
            cost_array.append(round(annual_payment,2))

    elif recur_checkbox_val == "true":
        annual_payment = float(const_cost)
        for j in range(recur_years):
            annual_payment = annual_payment * (inflation_rate + 1)
            cost_array.append(round(annual_payment, 2))

    # Create new Project record
    new_project = Project(
        id= row_id,
        latitude=latitude,
        longitude=longitude,
        facility_id=facility_id,
        project=project,
        est_year=est_year,
        est_cost=est_cost,
        category=category,
        description=description,
        priority=priority,
        const_year=const_year,
        const_cost=cost_array,
        debt_checkbox_val= debt_checkbox_val,
        recur_checkbox_val= recur_checkbox_val,
    )

    # Get connection/session to database
    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()

    # Add the new project record to the session
    session.add(new_project)

    # Commit the session and close the connection
    session.commit()
    session.close()


def add_new_project_from_csv(row_id, latitude, longitude, facility_id, project, est_cost, const_year, category, description, priority, est_year, const_cost, debt_checkbox_val, recur_checkbox_val):
    """
    Persist new project.
    """
    # Convert GeoJSON to Python dictionary

    inflation_rate = 0.04
    interest_rate = 0.04
    pay_period = 20
    recur_years = 20

    cost_array = []
    cost_array.append(const_cost)
    print(debt_checkbox_val)
    if debt_checkbox_val == "true":
        annual_payment = float(const_cost) * (
                (interest_rate * (1 + interest_rate) ** (pay_period)) / (
                (1 + interest_rate) ** (pay_period) - 1))
        for _ in range(pay_period-1):
            cost_array.append(round(annual_payment,2))

    elif recur_checkbox_val == "true":
        annual_payment = float(const_cost)
        for j in range(recur_years):
            annual_payment = annual_payment * (inflation_rate + 1)
            cost_array.append(round(annual_payment, 2))

    # Create new Project record
    new_project = Project(
        id= row_id,
        latitude=latitude,
        longitude=longitude,
        facility_id=facility_id,
        project=project,
        est_year=est_year,
        est_cost=est_cost,
        category=category,
        description=description,
        priority=priority,
        const_year=const_year,
        const_cost=cost_array,
        debt_checkbox_val= debt_checkbox_val,
        recur_checkbox_val= recur_checkbox_val,
    )

    # Get connection/session to database
    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()

    # Add the new project record to the session
    session.add(new_project)

    # Commit the session and close the connection
    session.commit()
    session.close()

def add_new_revenue(row_id, scenario, rev_src, mval, rev_year):
    """
    Persist new project.
    """
    # Convert GeoJSON to Python dictionary
    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()



    # Create new Project record
    new_revenue = Revenue(
        id=row_id,
        scenario=scenario,
        revenue_source=rev_src,
        monetary_Value=mval,
        year=rev_year,
    )

    # Get connection/session to database


    # Add the new project record to the session
    session.add(new_revenue)

    # Commit the session and close the connection
    session.commit()
    session.close()

def get_all_projects():
    """
    Get all persisted projects.
    """
    # Get connection/session to database
    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()

    # Query for all project records
    projects = session.query(Project).all()
    session.close()

    return projects

def get_all_revenue():
    """
    Get all persisted projects.
    """
    # Get connection/session to database
    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()

    # Query for all project records
    revenue = session.query(Revenue).all()
    session.close()

    return revenue

def init_primary_db(engine, first_time):
    """
    Initializer for the primary database.
    """
    # Create all the tables
    Base.metadata.create_all(engine)

    # Add data
    if first_time:
        # Make session
        Session = sessionmaker(bind=engine)
        session = Session()

        # Initialize database with two projects
        # project1 = Project(
        #     latitude=40.406624,
        #     longitude=-111.529133,
        #     facility_id="Deer Creek",
        #     project="New Intake",
        #     est_cost="1000",
        #     const_year="2022",
        #     category="Water",
        #     description="Replace Deer Creek intake structure",
        #     priority="4",
        #     est_year="2020",
        #     const_cost=["2000"],
        #     debt_checkbox_val=True,
        #     recur_checkbox_val=False,
        #
        # )
        #
        # project2 = Project(
        #     latitude=40.598168,
        #     longitude=-111.424055,
        #     facility_id="Jordanelle",
        #     project="Clean Water",
        #     est_cost="2000",
        #     const_year="2023",
        #     category="Stormwater",
        #     description="Clean up Jordanelle",
        #     priority="4",
        #     est_year="2020",
        #     const_cost=["5000"],
        #     debt_checkbox_val=False,
        #     recur_checkbox_val=True,
        # )

        # Add the projects to the session, commit, and close
        session.add(project1)
        session.add(project2)
        session.commit()
        session.close()