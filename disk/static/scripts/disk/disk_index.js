$(document).ready(function () {
    window.data = null;
    var oTable = new TableInit();
    oTable.Init();
    var oFileTable = new FileTableInit();
    oFileTable.Init();
    get_check_data();
    toastr.options.positionClass = 'toast-top-center';
    button_link();
    tableFocus();
    setTimeout(function () {
		document.getElementById("disk_id").click();
    },5);
});


var TableInit = function () {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {
        $('#table').bootstrapTable({
            url: '/disk/disk_info/',         //请求后台的URL（*）
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
            search: true,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
            strictSearch: true,
            showColumns: true,                  //是否显示所有的列
            showRefresh: true,                  //是否显示刷新按钮
            minimumCountColumns: 2,             //最少允许的列数
            clickToSelect: true,                //是否启用点击选中行
            // height: 500,                        //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
            // uniqueId: "ID",                     //每一行的唯一标识，一般为主键列
            showToggle: true,                    //是否显示详细视图和列表视图的切换按钮
            cardView: false,                    //是否显示详细视图
            detailView: false,                   //是否显示父子表
            columns: [{
                checkbox: true
            }, {
                field: 'disk_id',
                title: 'ID',
                visible: false
            }, {
                field: 'disk_name',
                title: '硬盘名称'
            }, {
                field: 'disk_type',
                title: '硬盘类型'
            }, {
                field: 'disk_size',
                title: '总大小'
            }, {
                field: 'disk_used',
                title: '已使用',
            }, {
                field: 'disk_avail',
                title: '可以使用',
            }, {
                field: 'disk_mount',
                title: '挂载目录',
                visible: false
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

var FileTableInit = function () {
    var oFileTableInit = new Object();
    //初始化Table
    oFileTableInit.Init = function () {
        $('#file_table').bootstrapTable({
            url: '/disk/file_info/',         //请求后台的URL（*）
            method: 'get',    //请求方式（*）
            toolbar: '#toolbar',                //工具按钮用哪个容器
            striped: true,                      //是否显示行间隔色
            cache: true,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
            pagination: true,                   //是否显示分页（*）
            sortable: true,                     //是否启用排序
            sortOrder: "asc",                   //排序方式
            queryParams: oFileTableInit.queryParams,//传递参数（*）
            sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
            pageNumber: 1,                       //初始化加载第一页，默认第一页
            pageSize: 10,                       //每页的记录行数（*）
            pageList: [10, 25, 50, 100],        //可供选择的每页的行数（*）
            search: true,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
            showExport: true,
            exportDataType: "basic",
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
                if (row.file_active_stat == "激活") {
                    strclass = 'success';//还有一个active
                }
                else if (row.file_active_stat == "未激活") {
                    strclass = 'danger';
                }
                else {
                    return {};
                }
                return { classes: strclass }
            },
            columns: [{
                checkbox: true
            }, {
                field: 'id',
                title: 'ID',
                visible: false
            }, {
                field: 'file_user',
                title: '用户'
            }, {
                field: 'file_group',
                title: '群组'
            }, {
                field: 'file_disk_type',
                title: '硬盘类型'
            }, {
                field: 'file_route',
                title: '文件路径',
            }, {
                field: 'file_share_name',
                title: '共享名称',
            }, {
                field: 'file_disk_name',
                title: '硬盘名称',
                visible: false
            },{
                field: 'file_cold_time',
                title: '冻结时间',
            },{
                field: 'file_add_time',
                title: '提交时间',
            },{
                field: 'file_time',
                title: '更新时间',
            },{
                field: 'file_active_stat',
                title: '激活状态',
            },{
                field: 'file_share_stat',
                title: '共享状态',
            },{
                field: 'operate',
                title: '操作',
                align: 'center',
                events: operateEvents,
                formatter: operateFormatter
            },],
        });
    };
        //得到查询的参数
    oFileTableInit.queryParams = function (params) {
        var temp = {   //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
            limit: params.limit,   //页面大小
            offset: params.offset,  //页码
        };
        return temp;
    };
    return oFileTableInit;
};
function operateFormatter(value, row, index) {
            return [
                '<button type="button" class="RoleOfD btn btn-default  btn-sm" style="margin-right:15px;">查看</button>',
            ].join('');
}
window.operateEvents = {
          'click .RoleOfD': function (e, value, row, index) {
                window.location.href = "/disk/file/" + row.id + "/"
         },};

function get_check_data() {
    $("#btn_print").click(function () {
        var a = $("#table").bootstrapTable('getSelections');
        if (a.length <= 0) {
            toastr.warning("请选中一行")
        } else {
            var b = JSON.stringify(a);
            console.log(b);
            var url = "/detail/change/";
            $.ajax({
                dataType: "json",
                traditional: true,//这使json格式的字符不会被转码
                data: {"data": b},
                type: "post",
                url: url,
                success: function (data, status) {
                    toastr.success(status);
                },
                error: function (data, status) {
                    toastr.error(status);
                }
            });
        }

    });

}


function button_link() {
    $("#disk_add").click(function () {
        window.location.href = "/disk/adddisk/"
    });
    $("#disk_del").click(function () {
        var arrselections = $("#table").bootstrapTable('getSelections');
        if (arrselections.length > 0) {
            var id = $.map(arrselections, function (row){return row.disk_id});

            $.ajax({
                type: "post",
                url: "/disk/change/",
                data: {"data": JSON.stringify({"msg": "disk_del", "id": id})},
                success: function () {
                    toastr.success("删除成功");
                    $("#table").bootstrapTable('refresh');
                },
                error: function () {
                    toastr.error("删除失败")
                },
            });
        }
        else {
            toastr.error("请选择数据")
        }
    });

    $("#file_create").click(function () {
        window.location.href = "/disk/createfile/"
    });

    $("#file_active").click(function () {
        var arrselections = $("#file_table").bootstrapTable('getSelections');
        if (arrselections.length > 0) {
            var id = $.map(arrselections, function (row){return row.id});
            $.ajax({
                type: "post",
                url: "/disk/change/",
                data: {"data": JSON.stringify({"msg": "active_change", "id": id})},
                success: function () {
                    toastr.success('激活状态更改成功');
                    $("#file_table").bootstrapTable('refresh');
                },
                error: function () {
                    toastr.error("更改失败")
                }
            })
        } else {
            toastr.warning('请选择有效数据');
        }
    });

    $("#start_share").click(function () {
         var arrselections = $("#file_table").bootstrapTable('getSelections');
        if (arrselections.length > 0) {
            var id = $.map(arrselections, function (row){return row.id});
            $.ajax({
                type: "post",
                url: "/disk/change/",
                data: {"data": JSON.stringify({"msg": "change_share", "id": id})},
                success: function () {
                    toastr.success('开启共享成功');
                    $("#file_table").bootstrapTable('refresh');
                },
                error: function () {
                    toastr.error("开启失败")
                }
            })
        } else {
            toastr.warning('请选择有效数据');
        }
    });

    $("#start_smb").click(function () {
         var arrselections = $("#file_table").bootstrapTable('getSelections');
        $("#start_share").click(function () {
            if (arrselections.length > 0) {
                var id = $.map(arrselections, function (row){return row.id});
                $.ajax({
                    type: "post",
                    url: "/disk/change/",
                    data: {"data": JSON.stringify({"msg": "change_smb", "id": id})},
                    success: function () {
                        toastr.success('开启共享成功');
                        $("#file_table").bootstrapTable('refresh');
                    },
                    error: function () {
                        toastr.error("开启失败")
                    }
                })
            } else {
                toastr.warning('请选择有效数据');
            }
        });
    });

     $("#file_del").click(function () {
           var arrselections = $("#file_table").bootstrapTable('getSelections');
           if (arrselections.length <= 0) {
               toastr.warning('请选择有效数据');
               return;
           }

           Ewin.confirm({ message: "确认要删除选择的数据吗？" }).on(function (e) {
               if (!e) {
                   return;
               }
               var id = $.map(arrselections, function (row){return row.id});
               $.ajax({
                   type: "post",
                   url: "/disk/change/",
                   data: { "data": JSON.stringify({"msg": "file_del", "id": id}) },
                   success: function (data, status) {
                       if (status === "success") {
                           toastr.success('删除配置成功');
                           $("#file_table").bootstrapTable('refresh');
                       }
                   },
                   error: function () {
                       toastr.error('Error');
                   },
                   complete: function () {

                   }
               });
           });
        });

     $("#disk_start_back").click(function () {
         toastr.success('开启备盘成功');
     });

      $("#disk_stop_back").click(function () {
         toastr.success('关闭备盘成功');
     });

}

function tableFocus() {
    $("#table1>tbody>tr").on("click", function () {
        // $(this).parent().find("tr.focus").toggleClass("focus");//取消原先选中行
        $(this).toggleClass("focus");//设定当前行为选中行
    });
}