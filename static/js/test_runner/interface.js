
$(document).ready(function(){

    $.api_request = function(editor){

        var form_data = $.get_form_data(editor);

        $.ajax({
            url: "/interface/run",
            method: "POST",
            data: form_data,
            success: function(data){
                var response = $("#interface_response");
                try {
                    var out = JSON.stringify(JSON.parse(data), null, 2);
                    response.text(out);
                    //l.stop();
                }catch (SyntaxError) {
                    response.text(data)
                }
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
                    window.location.reload();
                }else{
                    console.log(data);
                    alert(JSON.stringify(data.error));
                }
            }

        });


    };

    $.get_form_data = function(editor){

        var form_data = $("#interface_form").serializeArray();
        console.log(form_data);
        var type_select = $(".body_type.active").attr("id");
        var data_type = new Object();
        data_type["name"] = "data_type";
        data_type["value"] = type_select;

        form_data.push(data_type);

        if(type_select == "JSON_data_select"){

            var json = new Object();
            var json_data = editor.getText();
            console.log(json_data);
            json["name"] = "interface_json";
            json["value"] = json_data;
            form_data.push(json)

        }
        return form_data

    }

});
