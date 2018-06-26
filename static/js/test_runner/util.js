$(document).ready(function () {

    $.add_field = function (last_field) {
        var new_field = last_field.clone(true, true);

        var elem_id = last_field.find(":input")[0].id;
        var elem_num = parseInt(elem_id.replace(/.*-(\d{1,4})-.*/m, '$1')) + 1;

        new_field.find(":input").each(function () {
            var id = $(this).attr('id').replace('-' + (elem_num - 1) + '-', '-' + (elem_num) + '-');
            $(this).attr('name', id).attr('id', id).val('').removeAttr("checked");
        });

        last_field.after(new_field);
    };

    $.delete_field = function (delete_item, fields) {

        if (fields.length > 1) {
            var thisRow = delete_item.parent();
            thisRow.remove();
        }
    }



});
