$(document).ready(function () {
    var oTable = new TableInit();
    oTable.Init();
    buttonclick()
    toastr.options.positionClass = 'toast-top-center';
});


var TableInit = function () {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {
        $('#disk_manger_table').bootstrapTable({
            url: '/disk/diskMangerInfo/',         //请求后台的URL（*）
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
            // search: true,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
            strictSearch: true,
            // showColumns: true,                  //是否显示所有的列
            showRefresh: true,                  //是否显示刷新按钮
            minimumCountColumns: 2,             //最少允许的列数
            clickToSelect: true,                //是否启用点击选中行
            // height: 500,                        //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
            // uniqueId: "ID",                     //每一行的唯一标识，一般为主键列
            // showToggle: true,                    //是否显示详细视图和列表视图的切换按钮
            // cardView: false,                    //是否显示详细视图
            // detailView: false,                   //是否显示父子表
            rowStyle: function (row, index) {
                //这里有5个取值代表5中颜色['active', 'success', 'info', 'warning', 'danger'];
                var strclass = "";
                if (row.disk_off_stat == 0) {
                    strclass = 'success';//还有一个active
                }
                else if (row.disk_off_stat == 1) {
                    strclass = 'danger';
                }
                else {
                    return {};
                }
                return {classes: strclass}
            },
            columns: [{
                checkbox: true
            }, {
                field: 'id',
                title: 'ID',
                visible: false
            }, {
                field: 'disk_stat_name',
                title: '硬盘盘符'
            }, {
                field: 'disk_stat',
                title: '硬盘状态'
            }, {
                field: 'disk_slot',
                title: '硬盘槽位'
            }, {
                field: 'disk_off_stat',
                title: '关闭状态',
            }, {
                field: 'disk_uuid',
                title: 'UUID',
            }, {
               field: "disk_name",
               title: "硬盘名称"
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

function buttonclick() {
    $("#disk_start").click(function () {
        var  select = $("#disk_manger_table").bootstrapTable('getSelections');
        if (select.length<1){
            toastr.error("请选择数据");
            return;
        }
        var id = $.map(select, function (row){return row.id});
        var $btn = $(this).button('loading');
        $("#disk_stop").attr("disabled",true);
        $.ajax({
            type: "post",
            url: "",
            data: {"data": JSON.stringify({"msg": "start", "id": id})},
            success: function () {
                setTimeout(function () {
                    $btn.button('reset');
                    $("#disk_stop").removeAttr("disabled");
                    top.location.reload();
                }, 20000)
            }
        })
    });
    $("#disk_stop").click(function () {
        var select = $("#disk_manger_table").bootstrapTable('getSelections');
        if (select.length < 1) {
            toastr.error("请选择数据");
            return;
        }
        $("#disk_start").attr("disabled",true);
        var id = $.map(select, function (row){return row.id});
        var $btn = $(this).button('loading');
        $.ajax({
            type: "post",
            url: "",
            data: {"data": JSON.stringify({"msg": "stop", "id": id})},
            success: function () {
                setTimeout(function () {
                    $("#disk_start").removeAttr("disabled");
                    $btn.button('reset');
                    top.location.reload();
                }, 20000)
            }
        })
    });
}
