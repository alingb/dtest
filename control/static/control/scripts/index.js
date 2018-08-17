$(document).ready(function () {
    main();
});

function main() {
    $('#submit_post').on('click', function () {
        var $btn = $(this).button('loading');
        var arrselections = {};
        arrselections.ip = $("#ip").val();
        arrselections.cmd = $("#cmd").val();
        $.ajax({
            type: "post",
            url: "#",
            data: {"data": JSON.stringify(arrselections)},
            success: function (data, status) {
                toastr.success('提交数据成功');
                window.location.href = "/web";
            },
            error: function () {
                toastr.error('Error');
                $btn.button('reset');
            },
            }
        )
        }

    )
}
