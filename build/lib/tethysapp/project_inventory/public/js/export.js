$(function(){
    if(this.value == "CIP"){
            document.getElementById("gis-input").style.display = "none";
            document.getElementById("cip-input").style.display = "inline-block";
    } else {
        document.getElementById("gis-input").style.display = "inline-block";
        document.getElementById("cip-input").style.display = "none";
    }
    $(document.forms[0].elements.export_radio).change(function(){
        if(this.value == "CIP"){
            document.getElementById("gis-input").style.display = "none";
            document.getElementById("cip-input").style.display = "inline-block";
        } else {
            document.getElementById("gis-input").style.display = "inline-block";
            document.getElementById("cip-input").style.display = "none";
        }
    });
});