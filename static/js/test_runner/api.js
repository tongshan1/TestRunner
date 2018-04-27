/**
 * Created by tongshan on 2018/4/27.
 */
$(document).ready(function(){

    $.api_request = function(url, method, header, param){


        $.ajax({
            url: "/api/run",
            method: "POST",
            data: {
                "interface_url": url,
                "interface_method": method,
                "interface_header": header,
                "interface_body": param
            },
            success: function(data){
                alert("request success")
            }

        });
    };

    $.api_add = function(){

    }
});
