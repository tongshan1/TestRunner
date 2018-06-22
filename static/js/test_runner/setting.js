$(document).ready(function () {

    $.add_field = function () {
        var old_variable_field = $(".variable_field:last");
        var field = old_variable_field.clone(true, true);

        var elem_id = field.find(":input")[0].id;
        var elem_num = parseInt(elem_id.replace(/.*-(\d{1,4})-.*/m, '$1')) + 1;

        field.find(":input").each(function () {
            var id = $(this).attr('id').replace('-' + (elem_num - 1) + '-', '-' + (elem_num) + '-');
            $(this).attr('name', id).attr('id', id).val('').removeAttr("checked");
        });

        old_variable_field.after(field);
    };

    $.delete_field = function (delete_item) {
        var variable_field = $(".variable_field");

        if (variable_field.length > 1) {
            var thisRow = delete_item.parent();
            thisRow.remove();
        }
    }

});