$(document).ready(function () {

    $.init_request_data = function (data) {

        var request_data = new Object();

        for (var i = 0; i < data.length; i++) {
            request_data[data[i].name] = data[i].value;

        }
        return JSON.stringify(request_data)
    };

    $.api_request = function (l, url, method, header, query, param, verification) {

        var setting = $("#test_case_environment").attr("value");

        $.ajax({
            url: "/interface/run",
            method: "POST",
            data: {
                "setting": setting,
                "interface_url": url,
                "interface_method": method,
                "interface_header": header,
                "interface_query": query,
                "interface_body": param,
                "testcase_verification": verification
            },
            success: function (data) {
                try {
                    var container = document.getElementById('test_case_response');

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

    $.test_case_save = function (test_case_name, module_id, url, method, header, query, param, verification) {

        var csrf_token = $("#csrf_token").val();

        $.ajax({
            url: "/test_case_add.html",
            method: "POST",
            data: {
                "csrf_token": csrf_token,
                "testcase_name": test_case_name,
                "module_id": module_id,
                "interface_url": url,
                "testcase_method": method,
                "testcase_header": header,
                "testcase_query": query,
                "testcase_body": param,
                "testcase_verification": verification,
                "is_active": true
            },
            success: function (data) {
                if (data.ret == 1) {
                    alert("添加成功");
                    window.location.reload();
                } else {
                    alert(data.error);
                }
            }

        });

    };

    $.get_api_data = function () {

        var test_case_name = $("#test_case_name").val();
        var test_case_url = $("#test_case_url").val();
        var test_case_method = $("#test_case_method").text();
        var module_id = $("#test_case_module").attr("value");

        var headers = new Object();
        var head_key = $(".key_header_table");

        var query = new Object();
        var query_key = $(".key_query_table");

        var form_data = new Object();
        var form_data_key = $(".key_form_data");

        var urlencoded_data = new Object();
        var urlencoded_data_key = $(".key_urlencoded_data");

        var verification_data = new Object();
        var verification_data_key = $(".key_verification_data");


        $(head_key).each(function () {
            headers[$(this).val()] = $(this).parent().next("td").children(".value_header_table").val()

        });
        headers = JSON.stringify(headers);

        $(query_key).each(function () {
            query[$(this).val()] = $(this).parent().next("td").children(".value_query_table").val()

        });
        query = JSON.stringify(query);

        $(form_data_key).each(function () {
            form_data[$(this).val()] = $(this).parent().next("td").children(".value_form_data").val()

        });
        form_data = JSON.stringify(form_data);

        $(urlencoded_data_key).each(function () {
            urlencoded_data[$(this).val()] = $(this).parent().next("td").children(".value_urlencoded_data").val()

        });
        urlencoded_data = JSON.stringify(urlencoded_data);

        $(verification_data_key).each(function () {
            var verification_data_value = [];
            verification_data_value.push($(this).parent().next("td").children(".value_verification_data").val());
            verification_data_value.push($(".key_verification_data").parent().parent().children("td").children(".require_verification_data").is(":checked"));
            verification_data[$(this).val()] = verification_data_value;

        });
        verification_data = JSON.stringify(verification_data);


        return {
            "test_case_name": test_case_name,
            "test_case_url": test_case_url,
            "module_id": module_id,
            "test_case_method": test_case_method,
            "headers": headers,
            "form_data": form_data,
            "urlencoded_data": urlencoded_data,
            "verification_data": verification_data

        }
    };

    $.table_add_tr = function (table_id, key, value, description) {

        var table = document.getElementById(table_id);
        var row = table.insertRow(-1);
        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);
        var cell3 = row.insertCell(2);
        var cell4 = row.insertCell(3);
        cell1.innerHTML = '<input type="checkbox" class="require_' + table_id + '" checked>';
        cell2.innerHTML = '<input type="text" class="form-control key_' + table_id + '" value="' + key + '">';
        cell3.innerHTML = '<input type="text" class="form-control value_' + table_id + '" value="' + value + '">';
        cell4.innerHTML = '<input type="text" class="form-control description_' + table_id + '" value="' + description + '">';
    };


    $.table_delete_tr = function (table_id) {

        var table = document.getElementById(table_id);

        $(".require_" + table_id + ":checked").each(function () {

            var index = $(this).parent().parent().index();
            table.deleteRow(index);
        });

    };

    $.set_header_type = function (type) {

        var name = $("#header_table tbody tr:eq(0) td:eq(1) input");
        var value = $("#header_table tbody tr:eq(0) td:eq(2) input");

        name.val("Content-type");
        value.val(type);

    };

    $.load_interface = function (interfaces) {
        $(".test_case_module_interface_menu").html("");
        interfaces = $.parseJSON(interfaces);
        for (var i = 0; i <= interfaces.length; i++) {

            var data_id = interfaces[i].id;
            var data_name = interfaces[i].interface_name;
            $(".test_case_module_interface_menu").append("<li value=\"" + data_id + "\">" + data_name + "</li>")
        }

    };

    $.get_interface_by_module = function (module_id, load_data) {
        $.ajax({
            url: "/interface/module/" + module_id,
            method: "GET",
            success: function (data) {
                load_data(data)

            }
        });

    };

    $.load_interface_info = function (interface, json_editor) {
        interface = $.parseJSON(interface);
        $("#test_case_url").attr("value", interface.interface_url);
        $("#test_case_method").text(interface.interface_method);
        var headers = $.parseJSON(interface.interface_header);

        var header_Content_type = "";

        for (var x = 0; x < headers.length; x++) {

            $.table_add_tr("header_table", headers[x].name, headers[x].value, headers[x]["description"]);

            if(headers[x].name == "Content-type"){
                header_Content_type = headers[x].value
            }
        }

        if (header_Content_type == "application/form-data") {
            var body = $.parseJSON(interface.interface_body);
            var body_type = $("#form_data_a");

            for (var y = 0; y < body.length; y++) {
                $.table_add_tr("form_data", body[y].name, body[y].value, body[y]["description"]);
            }

            body_type.click()
        }

        if (header_Content_type == "application/x-www-form-urlencoded" || header_Content_type =="") {

            var body = $.parseJSON(interface.interface_body);
            var body_type = $("#urlencoded_data_a");

            for (var z = 0; z < body.length; z++) {
                $.table_add_tr("urlencoded_data", body[z].name, body[z].value, body[z]["description"]);
            }
            body_type.click()
        }

        if (header_Content_type == "application/json") {
            json_editor.setText(interface.interface_body);
            var body_type = $("#JSON_data_a");
            body_type.click()
        }


    };

    $.get_interface_by_id = function (interface_id, load_data, json_editor) {
        var interfaces;

        $.ajax({
            url: "/interface/" + interface_id,
            method: "GET",
            success: function (data) {
                load_data(data, json_editor)

            }
        });

        return interfaces
    };
});
