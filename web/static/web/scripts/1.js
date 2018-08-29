$(document).ready(function () {
    window.data = null;
    get_data();
    setdata();
    get_check_data();
        //2.初始化Button的点击事件
    var oButtonInit = new ButtonInit();
    oButtonInit.Init();
    toastr.options.positionClass = 'toast-top-center';
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
        toolbarAlign: "left",
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


function get_check_data() {
    $("#btn_print").click(function () {
        var a = $("#table").bootstrapTable('getSelections');
        if (a.length <= 0) {
            toastr.warning("请选中一行")
        } else {
            var b = JSON.stringify(a);
            console.log(b);
            var url = "${pageContext.request.contextPath}/login/datalist";
            $.ajax({
                dataType: "json",
                traditional: true,//这使json格式的字符不会被转码
                data: {"datalist": b},
                type: "post",
                url: url,
                success: function (data) {
                    toastr.success("成功！");
                },
                error: function (data) {
                    toastr.error(data.responseText);
                }
            });
        }

    });

}

var ButtonInit = function () {
    var oInit = new Object();
    var postdata = {};

    oInit.Init = function () {
        $("#btn_add").click(function () {
           $("#myModalLabel").text("新增");
           $("#myModal").find(".form-control").val("");
           $('#myModal').modal()

           postdata.DEPARTMENT_ID = "";
        });

        $("#btn_edit").click(function () {
           var arrselections = $("#table").bootstrapTable('getSelections');
           if (arrselections.length > 1) {
               toastr.warning('只能选择一行进行编辑');

               return;
           }
           if (arrselections.length <= 0) {
               toastr.warning('请选择有效数据');

               return;
           }
           $("#myModalLabel").text("编辑");
           $("#txt_departmentname").val(arrselections[0].DEPARTMENT_NAME);
           $("#txt_parentdepartment").val(arrselections[0].PARENT_ID);
           $("#txt_departmentlevel").val(arrselections[0].DEPARTMENT_LEVEL);
           $("#txt_statu").val(arrselections[0].STATUS);

           postdata.DEPARTMENT_ID = arrselections[0].DEPARTMENT_ID;
           $('#myModal').modal();
        });

        $("#btn_delete").click(function () {
           var arrselections = $("#table").bootstrapTable('getSelections');
           if (arrselections.length <= 0) {
               toastr.warning('请选择有效数据');
               return;
           }

           Ewin.confirm({ message: "确认要删除选择的数据吗？" }).on(function (e) {
               if (!e) {
                   return;
               }
               $.ajax({
                   type: "post",
                   url: "/Home/Delete",
                   data: { "": JSON.stringify(arrselections) },
                   success: function (data, status) {
                       if (status === "success") {
                           toastr.success('提交数据成功');
                           $("#table").bootstrapTable('refresh');
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

        $("#btn_submit").click(function () {
           postdata.DEPARTMENT_NAME = $("#txt_departmentname").val();
           postdata.PARENT_ID = $("#txt_parentdepartment").val();
           postdata.DEPARTMENT_LEVEL = $("#txt_departmentlevel").val();
           postdata.STATUS = $("#txt_statu").val();
           $.ajax({
               type: "post",
               url: "/Home/GetEdit",
               data: { "": JSON.stringify(postdata) },
               success: function (data, status) {
                   if (status === "success") {
                       toastr.success('提交数据成功');
                       $("#tb_departments").bootstrapTable('refresh');
                   }
               },
               error: function () {
                   toastr.error('Error');
               },
               complete: function () {

               }

           });
        });

        $("#btn_query").click(function () {
           $("#table").bootstrapTable('refresh');
        });
    };

    return oInit;
};

