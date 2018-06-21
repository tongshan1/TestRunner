$(document).ready(function () {


    $.get_interface_by_module = function (module_id) {

        $.ajax({
            url: "/interface/module/" + module_id,
            method: "GET",
            success: function (data) {
                var interface_select = $("#interface");
                interface_select.html("");
                var interfaces = $.parseJSON(data);
                interface_select.append("<option>请选择</option>");
                for (var i = 0; i < interfaces.length; i++) {

                    var data_id = interfaces[i].id;
                    var data_name = interfaces[i].interface_name;
                    interface_select.append("<option value=\"" + data_id + "\">" + data_name + "</option>")
                }

            }
        });

    };

    $.load_interface = function (interface_id, editor) {

        $.ajax({
            url: "/interface/" + interface_id,
            method: "GET",
            success: function (data) {
                $.load_data(data, editor)

            }
        });

    };

    $.load_data = function (data, editor) {
        //data 是一个interface对象 主要是设置header query body
        data = $.parseJSON(data);
        var method = data.interface_method;
        $("#testcase_method").val(method);
        var url = data.interface_url;
        $("#interface_url").val(url);
        // set header
        var headers = $.parseJSON(data.interface_header);
        var header_Content_type = "";
        for (var i = 0; i < headers.length; i++) {

            var button = $("#add_header");
            var input = $.set_field("header_field", button);
            input[0].value = headers[i].name;
            input[1].value = headers[i].value;

            if (headers[i].name == "Content-type") {
                header_Content_type = headers[i].value
            }

        }

        // set query
        alert(data.interface_query);
        var query = $.parseJSON(data.interface_query);
        for (var i = 0; i < query.length; i++) {

            var button = $("#add_query");
            var input = $.set_field("query_field", button);
            input[0].value = headers[i].name;
            input[1].value = headers[i].value;

        }

        // set body
        var body = $.parseJSON(data.interface_body);
        if (header_Content_type == "" || header_Content_type == "application/x-www-form-urlencoded") {

            for (var i = 0; i < body.length; i++) {
                var button = $("#add_urlencoded-data_field");
                var input = $.set_field("urlencoded-data_field", button);
                input[0].value = body[i].name;
                input[1].value = body[i].value;
            }

            var body_type = $("#urlencoded_data_a");
            body_type.click()

        }

        if (header_Content_type == "application/form-data") {

            for (var i = 0; i < body.length; i++) {
                var button = $("#add_form-data_field");
                var input = $.set_field("form-data_field", button);
                input[0].value = body[i].name;
                input[1].value = body[i].value;
            }

            var body_type = $("#form_data_a");
            body_type.click()

        }

        if (header_Content_type == "application/json") {

            editor.setText(body);

            var body_type = $("#JSON_data_a");
            body_type.click()

        }



    };

    $.set_field = function (field_div_class, add_button) {
        var field = $("." + field_div_class + ":last");
        var input_key = field.find(":input")[1];
        var input_value = field.find(":input")[2];

        if (input_key.value != "" || input_value.value != "") {
            add_button.click();
            field = $("." + field_div_class + ":last");
            input_key = field.find(":input")[1];
            input_value = field.find(":input")[2];
        }

        return [input_key, input_value];
    };


});