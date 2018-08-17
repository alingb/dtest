$(document).ready(function () {
    main();
});

function main() {
    alert("aa");
    $("#submit_post").click(function () {
        var arrselections = {};
        arrselections.ip = $("#ip").val();
        arrselections.cmd = $("#cmd").val();
        alert(JSON.stringify(arrselections));
        $.ajax({
            type: "post",
            url: "#",
            data: {"": JSON.stringify(arrselections)},
            success: function (data, status) {
                toastr.success('提交数据成功');
            },
            error: function () {
                toastr.error('Error');
            },
            }
        )
        }

    )
}
