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
    compbarcharts = document.querySelectorAll('.compare-barchart');
    for (var i = 0; i < compbarcharts.length; i++){
            compbarcharts[i].style.display = "none";
    };


    document.getElementById(rev_scenario+'-rev-barchart').style.display = "block";
    document.getElementById(rev_scenario+'-rev-compare-barchart').style.display = "block";

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

//document.onreadystatechange = function(e) {
//  if (document.readyState == "interactive") {
//    var all = document.getElementsByTagName("*");
//    for (var i = 0, max = all.length; i < max; i++) {
//      set_ele(all[i]);
//    }
//  }
//}
//
//function check_element(ele) {
//  var all = document.getElementsByTagName("*");
//  var totalele = all.length;
//  var per_inc = 100 / all.length;
//
//  if ($(ele).on()) {
//    var prog_width = per_inc + Number(document.getElementById("progress_width").value);
//    document.getElementById("progress_width").value = prog_width;
//    $("#bar1").animate({
//      width: prog_width + "%"
//    }, 10, function() {
//      if (document.getElementById("bar1").style.width == "100%") {
//        $(".progress").fadeOut("slow");
//      }
//    });
//  } else {
//    set_ele(ele);
//  }
//}
//
//function set_ele(set_element) {
//  check_element(set_element);
//}

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