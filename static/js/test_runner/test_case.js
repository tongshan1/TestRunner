/**
 * Created by tongshan on 2018/4/27.
 */
$(document).ready(function(){

    $.api_request = function(url, method, header, param){

        var response;

        $.ajax({
            url: "/interface/run",
            method: "POST",
            async: false,
            data: {
                "interface_url": url,
                "interface_method": method,
                "interface_header": header,
                "interface_body": param
            },
            success: function(data){
                response =  data;
            }

        });

        return response

    };

    $.test_case_save = function(test_case_name, module_id, url, method, header, param){

        var response;
        var csrf_token = $("#csrf_token").val();

        $.ajax({
            url: "/test_case",
            method: "POST",
            async: false,
            data: {
                "csrf_token": csrf_token,
                "test_case_name": test_case_name,
                "module_id":module_id,
                "interface_url": url,
                "test_case_method": method,
                "test_case_header": header,
                "test_case_body": param,
                "is_active": true
            },
            success: function(data){
                response =  data;
            }

        });

        return response

    };

    $.get_api_data = function(){

        var test_case_name = $("#test_case_name").val();
        var test_case_url = $("#test_case_url").val();
        var test_case_method = $("#test_case_method").text();
        var module_id = $("#test_case_module").attr("value");

        var headers = new Object();
        var head_key = $(".key_header_table");

        var form_data = new Object();
        var form_data_key = $(".key_form_data");

        var urlencoded_data = new Object();
        var urlencoded_data_key = $(".key_urlencoded_data");

        $(head_key).each(function(){
            headers[$(this).val()] = $(this).parent().next("td").children(".value_header_table").val()

        });
        headers = JSON.stringify(headers);

        $(form_data_key).each(function(){
            form_data[$(this).val()]= $(this).parent().next("td").children(".value_form_data").val()

        });
        form_data = JSON.stringify(form_data);

        $(urlencoded_data_key).each(function(){
            urlencoded_data[$(this).val()]= $(this).parent().next("td").children(".value_urlencoded_data").val()

        });
        urlencoded_data = JSON.stringify(urlencoded_data);


        return {
            "test_case_name": test_case_name,
            "test_case_url": test_case_url,
            "module_id":module_id,
            "test_case_method":test_case_method,
            "headers":headers,
            "form_data":form_data,
            "urlencoded_data":urlencoded_data

        }
    };

    $.table_add_tr = function(table_id, key, value){

        var table = document.getElementById(table_id);
        var row = table.insertRow(-1);
        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);
        var cell3 = row.insertCell(2);
        cell1.innerHTML = '<input type="checkbox" class="require_'+table_id+'" checked>';
        cell2.innerHTML = '<input type="text" class="form-control key_'+table_id+'" value="'+key+'">';
        cell3.innerHTML = '<input type="text" class="form-control value_'+table_id+'" value="'+value+'">';
    };

    $.table_delete_tr = function(table_id){

        var table = document.getElementById(table_id);

        $(".require_"+table_id+":checked").each(function(){

            var index = $(this).parent().parent().index();
            table.deleteRow(index);
        });

    };

    $.set_header_type = function(type){
        var key = $("#header_table tbody tr:eq(0) td:eq(1) input");
        var value = $("#header_table tbody tr:eq(0) td:eq(2) input");

        key.val("Content-type");
        value.val(type);

    };

    $.load_interface = function(interfaces){
        interfaces = $.parseJSON(interfaces);
        for(var i= 0; i <=interfaces.length; i++){
            $(".test_case_module_interface_menu").append("<li value=\""+interfaces[i].id+"\">"+interfaces[i].interface_name+"</li>")
        }

    };

    $.get_interface_by_module = function(module_id, load_data){
        var interfaces ;

        $.ajax({
            url:"/interface/module/"+module_id,
            method:"GET",
            success: function(data){
                load_data(data)

            }
        });

        return interfaces
    };

    $.load_interface_info = function(interface, json_editor){
        interface = $.parseJSON(interface);
        $("#test_case_url").attr("value", interface.interface_url);
        $("#test_case_method").text(interface.interface_method);
        var headers =$.parseJSON(interface.interface_header);

        for(var key in headers){
            $.table_add_tr("header_table", key, headers[key]);
        }

        if(headers["Content-type"] == "application/form-data"){
            var body = $.parseJSON(interface.interface_body);

            for (var key in body){
                $.table_add_tr("form_data", key, body[key]);
            }

        }

        if(headers["Content-type"] == "application/x-www-form-urlencoded"){
            var body = $.parseJSON(interface.interface_body);
            for (var key in body) {
                $.table_add_tr("urlencoded_data", key, body[key]);
            }
        }

        if(headers["Content-type"] == "application/json"){
            alert(interface.interface_body);
            json_editor.setText(interface.interface_body)
        }




    };

    $.get_interface_by_id = function(interface_id, load_data, json_editor){
        var interfaces ;

        $.ajax({
            url:"/interface/"+interface_id,
            method:"GET",
            success: function(data){
                load_data(data, json_editor)

            }
        });

        return interfaces
    };
});
