$(document).ready(function () {
    window.data = null;
    get_data();
    setdata();
});


function get_data() {
    $.ajax({
        type: "get",
        url: "/detail/detail/",
        async: false,
        success: function (callback) {
            if (callback.msg === 'success') {
                window.data = callback.data;
            }
        }
    });
}

function setdata() {
    $('#table').bootstrapTable({
        contentType: "application/json",//请求内容格式 默认是 application/json 自己根据格式自行服务端处理
        dataType: "json",//期待返回数据类型
        method: "GET",
        toolbar: '#toolbar',                //工具按钮用哪个容器
        striped: true,                      //是否显示行间隔色
        cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
        pagination: true,                   //是否显示分页（*）
        sortOrder: "asc",                   //排序方式
        sidePagination: "client",           //分页方式：client客户端分页，server服务端分页（*）
        pageNumber: 1,                       //初始化加载第一页，默认第一页
        pageSize: 10,                       //每页的记录行数（*）
        pageList: [10, 25, 50, 100],        //可供选择的每页的行数（*）
        search: true,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
        showColumns: true,                  //是否显示所有的列
        showRefresh: true,                  //是否显示刷新按钮
        minimumCountColumns: 2,             //最少允许的列数
        clickToSelect: true,                //是否启用点击选中行
        // height: 500,                        //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
        uniqueId: "tnum",
        buttonsAlign: "right",
        toolbarAlign: "right",
        undefinedText: '-',
        buttonsClass: 'btn',
        showToggle: true,
        columns: [{
            checkbox: true
        }, {
            field: 'sn',
            title: 'SN'
        }, {
            field: 'sn_1',
            title: 'SN_1'
        }, {
            field: 'bios',
            title: 'BIOS'
        }, {
            field: 'bmc',
            title: 'BMC'
        }, {
            field: 'name',
            title: 'NAME'
        }],
        data: window.data,
    });
}