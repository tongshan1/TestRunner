/**
 * Created by tongshan on 2018/5/10.
 */
$(document).ready(function(){

    $.table_add_tr = function(table_id){

        var table = document.getElementById(table_id);
        var row = table.insertRow(-1);
        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);
        var cell3 = row.insertCell(2);
        cell1.innerHTML = '<input type="checkbox" class="require_'+table_id+'" checked>';
        cell2.innerHTML = '<input type="text" class="form-control key_'+table_id+'">';
        cell3.innerHTML = '<input type="text" class="form-control value_'+table_id+'">';
    };

});
