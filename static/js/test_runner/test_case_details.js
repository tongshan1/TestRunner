$(document).ready(function(){

    $.add_test_case = function(){

        var testcase_group_id = $("#testcase_group_id").val();
        var testcase_id = $("#test_case_module_interface").attr("value");
        var is_active = $("#is_active").is(":checked");
        var csrf_token = $("#csrf_token").val();


        $.ajax({
            url:"/testcase_testgroup",
            method: "POST",
            data:{
                "testcase_group_id":testcase_group_id,
                "testcase_id":testcase_id,
                "is_active":is_active,
                "csrf_token":csrf_token

            },
            success: function(data){
                if(data.ret == 1){
                    alert("添加成功！");
                    window.location.reload();
                }else{
                    alert("添加失败！")
                }
            }
        })
    };

    $.load_interface = function(testcase){
        $(".test_case_module_interface_menu").html("");
        testcase = $.parseJSON(testcase);
        for(var i= 0; i <=testcase.length; i++){
            $(".test_case_module_interface_menu").append("<li value=\""+testcase[i].id+"\">"+testcase[i].testcase_name+"</li>")
        }

    };

     $.get_test_case_by_module = function(module_id, load_data){
        var interfaces ;

        $.ajax({
            url:"/testcase/module/"+module_id,
            method:"GET",
            success: function(data){
                load_data(data)

            }
        });

        return interfaces
    };

    $.delete_cases = function(table_id){

        var table = document.getElementById(table_id);

        $(".test_case_check:checked").each(function(){

            var index = $(this).parent().parent().index();
            table.deleteRow(index);

            var case_id = $(this).attr("value");
            $.delete_case(case_id);
        });

    };

    $.delete_case = function(case_id){
        $.ajax({
            url:"/testcase_testgroup/"+case_id+"/delete",
            method:"DELETE",
            success: function(data){
                if(data.ret ==1){
                    alert("删除成功！");
                    window.location.reload();
                }else{
                    alert("删除失败！")
                }

            }
        });
    }
});
