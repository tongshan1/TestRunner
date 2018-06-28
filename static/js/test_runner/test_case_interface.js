$(document).ready(function () {

    $.api_request = function (editor) {

        var form_data = $.get_form_data(editor);

        console.log(form_data);

        $.ajax({
            url: "/testcase/run",
            method: "POST",
            data: form_data,
            success: function (data) {
                var response = $("#test_case_response");
                try {
                    var out = JSON.stringify(JSON.parse(data), null, 2);
                    response.text(out);
                    //l.stop();
                }catch (SyntaxError) {
                    response.text(data)
                }

                l.stop();
            }

        });


    };

    $.api_save = function (editor) {

        var form_data = $.get_form_data(editor);


        $.ajax({
            url: "#",
            method: "POST",
            data: form_data,
            success: function (data) {
                if(data.ret ==1){
                    alert("添加成功");
                    window.location.reload();
                }else{
                    console.log(data);
                    alert(JSON.stringify(data.error));
                }

            }

        });


    };


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
        var add_header = $("#add_header");
        $.remove_field("header_field", add_header);
        var headers = $.parseJSON(data.interface_header);
        var header_Content_type = "";
        for (var i = 0; i < headers.length; i++) {

            var input = $.set_field("header_field", add_header);
            input[0].value = headers[i].name;
            input[1].value = headers[i].value;

            if (headers[i].name == "Content-type") {
                header_Content_type = headers[i].value
            }

        }

        // set query
        var add_query = $("#add_query");
        $.remove_field("query_field", add_query);
        var query = $.parseJSON(data.interface_query);
        for (var i = 0; i < query.length; i++) {

            var input = $.set_field("query_field", add_query);
            input[0].value = query[i].name;
            input[1].value = query[i].value;

        }

        // set body
        var add_form_data_field = $("#add_form-data_field");
        $.remove_field("form-data_field", add_form_data_field);
        var body = $.parseJSON(data.interface_body);
        if (header_Content_type != "application/json") {
            for (var i = 0; i < body.length; i++) {

                var input = $.set_field("form-data_field", add_form_data_field);
                input[0].value = body[i].name;
                input[1].value = body[i].value;
            }

            var body_type = $("#form_data_a");
            body_type.click()

        }else{

            var json_data = new Object();

            for (var i = 0; i < body.length; i++) {
                json_data[body[i].name] = body[i].value
            }

            console.log(json_data);

            editor.setText(JSON.stringify(json_data));

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

    $.remove_field = function(field_div_class, add_button){
        // 判断最后一个是不是空的， 如果不是先添加一个空的 然后再删除
        var field = $("." + field_div_class + ":last");
        var input_key = field.find(":input")[1];
        var input_value = field.find(":input")[2];

        if (input_key.value != "" || input_value.value != "") {

            add_button.click();
        }
        var fields = $("." + field_div_class );

        for(var i=0; i<fields.length-1; i++){
            fields[i].remove()
        }

    };

    $.get_form_data = function(editor){

        var form_data = $("#test_case_form").serializeArray();
        var type_select = $(".body_type.active").attr("id");
        var data_type = new Object();
        data_type["name"] = "data_type";
        data_type["value"] = type_select;


        form_data.push(data_type);
        if(type_select == "JSON_data_select"){

            var json = new Object();
            var json_data = editor.getText();
            json["name"] = "testcase_json";
            json["value"] = json_data;
            form_data.push(json)

        }
        return form_data

    }


});