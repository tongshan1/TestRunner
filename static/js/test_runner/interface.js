
$(document).ready(function(){

    $.api_request = function(l, url, method, header, param){


        $.ajax({
            url: "/interface/run",
            method: "POST",
            data: {
                "interface_url": url,
                "interface_method": method,
                "interface_header": header,
                "interface_body": param
            },
            success: function(data){
                try {
                    var container = document.getElementById('interface_response');

                    container.innerHTML = "";

                    var options = {
                        mode: 'view'
                    };
                    var editor = new JSONEditor(container, options, JSON.parse(data));

                    editor.expandAll();
                } catch (SyntaxError) {
                    alert("请求失败！")
                }

                l.stop();
            }

        });


    };

    $.api_save = function(interface_name,module_id,  url, method, header, param){

        var csrf_token = $("#csrf_token").val();

        $.ajax({
            url: "/interface",
            method: "POST",
            data: {
                "csrf_token": csrf_token,
                "interface_name": interface_name,
                "module_id":module_id,
                "interface_url": url,
                "interface_method": method,
                "interface_header": header,
                "interface_body": param,
                "is_active": true
            },
            success: function(data){
                if (data.ret == 1){
                    alert("添加成功");
                    window.location.href = "/interface_list.html";
                }else{
                    alert(data.error);
                }
            }

        });


    };

    $.get_api_data = function(){

        var interface_name = $("#interface_name").val();
        var module_id = $("#module_id").val();
        var interface_url = $("#interface_url").val();
        var interface_method = $("#interface_method").text();

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
            "interface_name": interface_name,
            "module_id": module_id,
            "interface_url": interface_url,
            "interface_method":interface_method,
            "headers":headers,
            "form_data":form_data,
            "urlencoded_data":urlencoded_data

        }
    };

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


});
