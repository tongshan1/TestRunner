//Flot Pie Chart
$(function() {

    var fail = parseInt($("#fail").text());
    var success = parseInt($("#success").text());
    var error = parseInt($("#error").text());
    var total = parseInt($("#total").text());
    var other = total-fail-success-error;
    var pass_percent = (Math.round(success / total * 10000) / 100.00 + "%");

    $("#count_pass").text(pass_percent);

    var data = [{
        label: "其他",
        data: other
    }, {
        label: "失败用例",
        data: fail
    }, {
        label: "错误用例",
        data: error
    }, {
        label: "通过用例",
        data: success
    }];

    var plotObj = $.plot($("#flot-pie-chart"), data, {
        series: {
            pie: {
                show: true
            }
        },
        grid: {
            hoverable: true
        },
        tooltip: true,
        tooltipOpts: {
            content: "%p.0%, %s", // show percentages, rounding to 2 decimal places
            shifts: {
                x: 20,
                y: 0
            },
            defaultTheme: false
        }
    });

});


