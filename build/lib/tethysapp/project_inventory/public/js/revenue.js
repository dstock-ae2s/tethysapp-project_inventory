$(function(){
    hideShowPlotlyGraphs();
    $('#graph-selector').change(function(){hideShowPlotlyGraphs();});

});
function hideShowPlotlyGraphs(){
    var rev_scenario = $('#graph-selector').val();

    barcharts = document.querySelectorAll('.barchart');
    for (var i = 0; i < barcharts.length; i++){
            barcharts[i].style.display = "none";
    };

    piecharts = document.querySelectorAll('.piechart');
    for (var i = 0; i < piecharts.length; i++){
            piecharts[i].style.display = "none";
    };


    document.getElementById(rev_scenario+'-rev-barchart').style.display = "block";
    document.getElementById(rev_scenario+'-rev-piechart').style.display = "block";

//    }
//    else if (rev_scenario == "medium"){
//        document.getElementById('medium-rev-barchart').style.display = "block";
//        document.getElementById('medium-rev-piechart').style.display = "block";
//
//    }
//    else if (rev_scenario == "high"){
//        document.getElementById('high-rev-barchart').style.display = "block";
//        document.getElementById('high-rev-piechart').style.display = "block";
//
//    };

};

//function deletePlotlyGraphs(){
//    var graphdivs = document.querySelectorAll('.plotly-graph-div');
//    for (var i = 0; i < graphdivs.length; i++){
//        var graphid = graphdivs[i].id;
//        Plotly.purge(graphid);
//
//    };
//    var rev_scenario = document.getElementById('graph-selector').value;
//    var start_date = document.getElementById('graph-start-date').value;
//    var end_date = document.getElementById('graph-end-date').value;
//
//    console.log(rev_scenario+','+start_date+','+end_date);
//
//    var data = new FormData();
//    data.append('rev_scenario',rev_scenario);
//    data.append('start_date',start_date);
//    data.append('end_date',end_date);
//
//    var reload_plolty_graphs = ajax_update_database_with_file("reload-plotly-graphs", data); //Submitting the data through the ajax function, see main.js for the helper function.
//    reload_plolty_graphs.done(function(return_data){ //Reset the form once the data is added successfully
//
//
//
//
//    });

//};