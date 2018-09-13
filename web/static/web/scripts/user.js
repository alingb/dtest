$(document).ready(function () {
    var oTable = new TableInit();
    oTable.Init();
});


var TableInit = function () {
    var oTableInit = {};
    //初始化Table
    oTableInit.Init = function () {
        $('#user_table_id').bootstrapTable({
            url: '/web/get_info/user',         //请求后台的URL（*）
            method: 'get',    //请求方式（*）
            toolbar: '#toolbar',                //工具按钮用哪个容器
            striped: true,                      //是否显示行间隔色
            cache: true,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
            pagination: true,                   //是否显示分页（*）
            sortable: true,                     //是否启用排序
            sortOrder: "asc",                   //排序方式
            queryParams: oTableInit.queryParams,//传递参数（*）
            sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
            pageNumber: 1,                       //初始化加载第一页，默认第一页
            pageSize: 10,                       //每页的记录行数（*）
            pageList: [10, 25, 50, 100],        //可供选择的每页的行数（*）
            showRefresh: true,                  //是否显示刷新按钮
            minimumCountColumns: 2,             //最少允许的列数
            clickToSelect: true,                //是否启用点击选中行
            columns: [{
                field: 'username',
                title: '名称',
            }, {
                field: 'last_login',
                title: '最后一次登入'
            }, {
                field: 'date_joined',
                title: '创建时间'
            }, {
                field: 'operate',
                title: '操作',
                align: 'center',
                events: operateEvents,
                formatter: operateFormatter
            },],
        });
    };
    //得到查询的参数
    oTableInit.queryParams = function (params) {
        var temp = {   //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
            limit: params.limit,   //页面大小
            offset: params.offset,  //页码
        };
        return temp;
    };
    return oTableInit;
};

function operateFormatter(value, row, index) {
    return [
        '<button type="button" class="RoleOfD btn btn-default  btn-sm" style="margin-right:15px;">更改密码</button>',
        '<button type="button" class="RoleOfE btn btn-default  btn-sm" style="margin-right:15px;">删除</button>',
    ].join('');
}

window.operateEvents = {
    'click .RoleOfD': function (e, value, row, index) {
        alert(row.id)
    },
    'click .RoleOfE': function (e, value, row, index) {
        alert("delete");
    },
};
