/**
 * Created by tongshan on 2018/4/27.
 */
$(document).ready(function(){

    $.api_request = function(url, method, header, param){

        var response;

        $.ajax({
            url: "/api/run",
            method: "POST",
            async: false,
            data: {
                "interface_url": url,
                "interface_method": method,
                "interface_header": header,
                "interface_body": param
            },
            success: function(data){
                alert(data);
                response =  data;
            }

        });

        return response

    };

    $.api_add = function(){

    }
});
