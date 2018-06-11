
$(document).ready(function(){

    $.init_request_data = function(data){

        var request_data = new Object();

        for(var i= 0;i<data.length;i++){
            request_data[data[i].name] = data[i].value;

        }
        return JSON.stringify(request_data)
    };

    $.api_request = function(l, url, method, header, query, param){

        header = $.init_request_data(header);
        param = $.init_request_data(param);
        query = $.init_request_data(query);


        $.ajax({
            url: "/interface/run",
            method: "POST",
            data: {
                "interface_url": url,
                "interface_method": method,
                "interface_header":  header,
                "interface_query": query,
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
                    alert(data);
                    alert("请求失败！")
                }

                l.stop();
            }

        });


    };

    $.api_save = function(interface_name,interface_desc,module_id,  url, method, header, query, param){


        var csrf_token = $("#csrf_token").val();

        $.ajax({
            url: "/interface",
            method: "POST",
            data: {
                "csrf_token": csrf_token,
                "interface_name": interface_name,
                "interface_desc":interface_desc,
                "module_id":module_id,
                "interface_url": url,
                "interface_method": method,
                "interface_header":  JSON.stringify(header),
                "interface_query":  JSON.stringify(query),
                "interface_body":  JSON.stringify(param),
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
        var interface_desc = $("#interface_desc").val();

        var headers = [];
        var head_key = $(".key_header_table");

        var query = [];
        var query_key = $(".key_query_table");

        var form_data = [];
        var form_data_key = $(".key_form_data");

        var urlencoded_data = [];
        var urlencoded_data_key = $(".key_urlencoded_data");

        $(head_key).each(function(){
            var header = new Object();
            header["name"] = $(this).val();
            header["value"] = $(this).parent().next("td").children(".value_header_table").val();
            header["description"] = $(this).parent().next("td").next("td").children(".description_header_table").val();
            //headers[$(this).val()] = $(this).parent().next("td").children(".value_header_table").val()
            headers.push(header)

        });
        //headers = JSON.stringify(headers);

        $(query_key).each(function(){
            var data = new Object();
            data["name"] = $(this).val();
            data["value"] = $(this).parent().next("td").children(".value_query_table").val();
            data["description"] = $(this).parent().next("td").next("td").children(".description_query_table").val();
            //headers[$(this).val()] = $(this).parent().next("td").children(".value_header_table").val()
            query.push(data)

        });

        //query = JSON.stringify(query);

        $(form_data_key).each(function(){
            var data = new Object();
            data["name"] = $(this).val();
            data["value"] = $(this).parent().next("td").children(".value_form_data").val();
            data["description"] = $(this).parent().next("td").next("td").children(".description_form_data").val();
            //form_data[$(this).val()]= $(this).parent().next("td").children(".value_form_data").val()
            form_data.push(data)

        });
        //form_data = JSON.stringify(form_data);

        $(urlencoded_data_key).each(function(){

            var data = new Object();
            data["name"] = $(this).val();
            data["value"] = $(this).parent().next("td").children(".value_urlencoded_data").val();
            data["description"] = $(this).parent().next("td").children(".description_urlencoded_data").val();
            //urlencoded_data[$(this).val()]= $(this).parent().next("td").children(".value_urlencoded_data").val()
            urlencoded_data.push(data)

        });
        //urlencoded_data = JSON.stringify(urlencoded_data);


        return {
            "interface_name": interface_name,
            "interface_desc": interface_desc,
            "module_id": module_id,
            "interface_url": interface_url,
            "interface_method":interface_method,
            "headers":headers,
            "query":query,
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
        var cell4 = row.insertCell(3);
        cell1.innerHTML = '<input type="checkbox" class="require_'+table_id+'" checked>';
        cell2.innerHTML = '<input type="text" class="form-control key_'+table_id+'">';
        cell3.innerHTML = '<input type="text" class="form-control value_'+table_id+'">';
        cell4.innerHTML = '<input type="text" class="form-control description_'+table_id+'">';
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
