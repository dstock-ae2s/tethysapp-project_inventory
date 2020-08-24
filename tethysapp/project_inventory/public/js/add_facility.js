$(function(){
    $('#est_cost').change(function(){updateConstCost();});
    $('#est_year').change(function(){updateConstCost();});
    $('#const_year').change(function(){updateConstCost();});
    $('#debt-checkbox').change(function(){
        if(document.getElementById('debt-checkbox').checked == true){
            document.getElementById('recur-checkbox').checked = false;
        }
    });
    $('#recur-checkbox').change(function(){
        if(document.getElementById('recur-checkbox').checked == true){
            document.getElementById('debt-checkbox').checked = false;
        }
    });
});

function updateConstCost(){
    this_est_cost = parseFloat(document.getElementById('est_cost').value)
    this_const_year = parseFloat(document.getElementById('const_year').value)
    this_est_year = parseFloat(document.getElementById('est_year').value)
    document.getElementById('const_cost').value = ((this_est_cost*Math.pow(1.04,(this_const_year-this_est_year))).toFixed(0)).toString();
};

function addProjectRow (){
    console.log("In Add Project Row")

    var html = '';

        var nrows = document.querySelectorAll('.project-name');
        numrows = nrows.length;
        console.log(numrows);
        i = numrows;

        html += '<tr id="add-project-row-'+(i)+'">'+
                    '<td><input style="border: 1px solid" class="edit-fields project-name" type="text" id="' + (i) +'-add-project-project-name" name="' + (i) +'_add_project_project_name" value="" ></td>' +
                    '<td><input style="border: 1px solid" class="edit-fields" type="text" id="' + (i) +'-add-project-project-category" name="' + (i) +'_add_project_project_category" value="" ></td>' +
                    '<td><input style="border: 1px solid" class="edit-fields" type="text" id="' + (i) +'-add-project-project-priority" name="' + (i) +'_add_project_project_priority" value="" ></td>' +
                    '<td><input style="border: 1px solid" class="edit-fields" type="text" id="' + (i) +'-add-project-project-description" name="' + (i) +'_add_project_project_description" value="" ></td>' +
                    '<td><input style="border: 1px solid" class="edit-fields" type="text" id="' + (i) +'-add-project-project-estyear" name="' + (i) +'_add_project_project_estyear" value="" ></td>' +
                    '<td><input style="border: 1px solid" class="edit-fields" type="text" id="' + (i) +'-add-project-project-estcost" name="' + (i) +'_add_project_project_estcost" value="" ></td>' +
                    '<td><input style="border: 1px solid" class="edit-fields" type="text" id="' + (i) +'-add-project-project-constyear" name="' + (i) +'_add_project_project_constyear" value="" ></td>' +
                    '<td><input style="border: 1px solid" class="edit-fields" type="text" id="' + (i) +'-add-project-project-constcost" name="' + (i) +'_add_project_project_constcost" value="" ></td>' +
                    '<td><input class="edit-fields" type="checkbox" id="' + (i) +'-add-project-debt-checkbox" name="' + (i) +'_add_project_debt_checkbox" value="true"></td>' +
                    '<td><input class="edit-fields" type="checkbox" id="' + (i) +'-add-project-recur-checkbox" name="' + (i) +'_add_project_recur_checkbox" value="true"></td>' +
                    '<a name="submit-delete-region" id="delete-button-'+(i)+'" class="btn btn-danger submit-delete-region" role="button">'+
                    '<span class="glyphicon glyphicon-remove"></span> Delete </a>'+
                    '</div>'+
                    '</td>'+
                '</tr>';

    $('#add-project-list-table tr').last().after(html);
    j=numrows

    $('#'+j+'-add-project-project-estcost').change(function(){updateConstCost(j);});
    $('#'+j+'-add-project-project-estyear').change(function(){updateConstCost(j);});
    $('#'+j+'-add-project-project-constyear').change(function(){updateConstCost(j);});

    $('#'+j+'-add-project-debt-checkbox').change(function(){
        if(document.getElementById(j+'-add-project-debt-checkbox').value =="true"){
            document.getElementById(j+'-add-project-recur-checkbox').checked = false;
        }
        else{
            console.log(document.getElementById(j+'-add-project-debt-checkbox').value)
        }
    });
    $('#'+j+'-add-project-recur-checkbox').change(function(){
        if(document.getElementById(j+'-add-project-recur-checkbox').value == "true"){
            document.getElementById(j+'-add-project-debt-checkbox').checked = false;
        }
        else{
            console.log(document.getElementById(j+'-add-project-recur-checkbox').value)
        }
    });
};