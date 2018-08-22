$(document).ready(function () {
main();
});


function main() {
    tableFocus();
    showLineNum();
}

function tableFocus() {
    $("#disk_choose>tbody>tr").on("click", function () {
        $(this).parent().find("tr.focus").toggleClass("focus");//取消原先选中行
        $(this).toggleClass("focus");//设定当前行为选中行
    });
}
function setLineNum(line){
    if (typeof(line) !== "undefined ") {
//只要保证那个隐藏的INPUT存在,这里就不再判断是否存在了.
        $("#disk_name").val(line.id);
// document.getElementById("line_num").value = line.id;
    }
    else {
        alert('缺少参数');
    }
}
function showLineNum(){
//只要保证那个隐藏的INPUT存在,这里也不再判断是否存在了.
// var line_num = document.getElementById("line_num").value;
    const line_num = $("#line_num").val();
    // alert('上次点击的是第'+line_num+'行');
}