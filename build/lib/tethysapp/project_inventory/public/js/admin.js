function importProjectsToDb(){
    var data = new FormData();
    var import_projects_to_db = ajax_update_database_with_file("import-projects-to-db", data); //Submitting the data through the ajax function, see main.js for the helper function.
    import_projects_to_db.done(function(return_data){ //Reset the form once the data is added successfully
    });

}

function importRevenueToDb(){
    var data = new FormData();
    var import_revenue_to_db = ajax_update_database_with_file("import-revenue-to-db", data); //Submitting the data through the ajax function, see main.js for the helper function.
    import_revenue_to_db.done(function(return_data){ //Reset the form once the data is added successfully
    });

}
