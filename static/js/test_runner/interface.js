
$(document).ready(function(){

    $.api_request = function(editor){

        var form_data = $.get_form_data(editor);

        $.ajax({
            url: "/interface/run",
            method: "POST",
            data: form_data,
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

                //l.stop();
            }

        });


    };

    $.api_save = function(editor){

        var form_data = $.get_form_data(editor);

        $.ajax({
            url: "#",
            method: "POST",
            data: form_data,
            success: function(data){
                if (data.ret == 1){
                    alert("添加成功！");
                    window.location.href = "/interface_list.html";
                }else{
                    alert(data.error);
                }
            }

        });


    };

    $.get_form_data = function(editor){

        var form_data = $("#interface_form").serializeArray();
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
