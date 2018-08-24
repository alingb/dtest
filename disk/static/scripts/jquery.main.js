$(document).ready(function () {
    //original field values
    toastr.options.positionClass = 'toast-top-center';
    // var field_values = {
    //     //id        :  value
    //     'username': 'username',
    //     'password': 'password',
    //     'cpassword': 'password',
    //     'firstname': 'first name',
    //     'lastname': 'last name',
    //     'email': 'email address'
    // };
    //inputfocus
    // $('input#username').inputfocus({ value: field_values['username'] });
    // $('input#password').inputfocus({ value: field_values['password'] });
    // $('input#cpassword').inputfocus({ value: field_values['cpassword'] });
    // $('input#lastname').inputfocus({ value: field_values['lastname'] });
    // $('input#firstname').inputfocus({ value: field_values['firstname'] });
    // $('input#email').inputfocus({ value: field_values['email'] });


    //first_step
    $('form').submit(function () {
        return false;
    });
    $('#submit_first').click(function () {
        //remove classes
        $('#first_step input').removeClass('error').removeClass('valid');
        //ckeck if inputs aren't empty


        var fields = $('#first_step input[type=text]');
        var error = 0;
        fields.each(function () {
            var value = $(this).val();
            if (value.length < 1) {
                $(this).addClass('error');
                $(this).effect("shake", {times: 3}, 50);
                error++;
            } else {
                $(this).addClass('valid');
            }
        });

        if (!error) {
            var route = $("#route").val();
            if (route.indexOf("/") == -1) {
                toastr.error('路径非法，路径需要包含"/"');
                return;
            }
            $.ajax({
                type: "post",
                url: "/disk/checkroute/",
                data: {"data": JSON.stringify({"route": route})},
                success: function () {
                    //slide steps
                    $('#first_step').slideUp();
                    $('#second_step').slideDown();
                },
                error: function (data, status) {
                    toastr.error('路径已存在');
                },
            });
        } else {
            toastr.error("请输入信息");
            return false;
        }
    });


    $("#submit_second_pre").click(function () {
        $('#second_step').slideUp();
        $('#first_step').slideDown();

    });
    $('#submit_second').click(function () {
        var disk_type = $("#disk_type option:selected").val();
        var route = $("#route").val();
        var share_name = $("#share_name").val();
        var disk_name = $("#disk_name").val();
        console.log(disk_name);
        $("#disk_type_change").text(disk_type);
        $("#share_name_change").text(share_name);
        //remove classes
        $('#second_step input').removeClass('error').removeClass('valid');

        var fields = disk_name;
        var error = 0
        if (fields === "null") {
            error++;
        } else {
            $(this).addClass('valid');
        }
        if (!error) {
            //slide steps
            $('#second_step').slideUp();
            $('#third_step').slideDown();
        } else {
            toastr.error("请选择一个硬盘");
            return false
        }
    });


    $("#submit_third_pre").click(function () {
        $('#third_step').slideUp();
        $('#second_step').slideDown();

    });
    $('#submit_third').click(function () {
        var oTable = new TableInit();
        oTable.Init();
        //slide steps
        $('#third_step').slideUp();
        $('#fourth_step').slideDown();
        //prepare the fourth step
        // var fields = [$('#username').val(),
        //     $('#password').val(),
        //     $('#email').val(),
        //     $('#firstname').val() + ' ' + $('#lastname').val(),
        //     $('#age').val(),
        //     $('#gender').val(),
        //     $('#country').val()];
        // var tr = $('#fourth_step tr');
        // tr.each(function () {
        //     //alert( fields[$(this).index()] )
        //     $(this).children('td:nth-child(2)').html(fields[$(this).index()]);
        // });

    });

    $("#submit_fourth_pre").click(function () {
        $('#fourth_step').slideUp();
        $('#third_step').slideDown();

    });
    $("#create_group").click(function () {
        $("#myModalLabel").text("新增群组");
        $("#myModal").find("#txt_name").val("");
        $('#myModal').modal()
    });
    $("#group_submit").click(function () {
        var group_name = $("#txt_name").val();
        $.ajax({
            type: "post",
            url: "/disk/changegroup/",
            data: {"data": JSON.stringify({"group": group_name})},
            success: function (data, status) {
                toastr.success('群组创建成功');
                $("#group_show").bootstrapTable('refresh');
                $("#group_close").click();
            },
            error: function (data, status) {
                toastr.error('群组已存在');
                return false;
            }

        })
    });
    $('#submit_fourth').click(function () {
        var filedata = {};
        var disk_type = $("#disk_type option:selected").val();
        var route = $("#route").val();
        var share_name = $("#share_name").val();
        var disk_name = $("#disk_name").val();
        var cold_time = $("#cold_time option").val();
        var a = $("#group_show").bootstrapTable('getSelections');
        console.log(a);
        //send information to server
        if (a == "undefined" || a == "" || a == "null") {
            toastr.error('请选择群组');
        }
        else {
            var b = $.parseJSON(JSON.stringify(a))[0]["group_name"];
            filedata.file_disk_type = disk_type;
            filedata.file_route = route;
            filedata.file_share_name = share_name;
            filedata.file_disk_name = disk_name;
            filedata.file_cold_time = cold_time;
            filedata.file_group_name = b;
            $.ajax({
                type: "post",
                url: "/disk/changefile/",
                data: {"data": JSON.stringify(filedata)},
                success: function (data, status) {
                    toastr.success('提交数据成功');
                    window.location.href = "/disk/filemanger"
                },
                error: function () {
                    toastr.error('Error');
                },
            });
        }
    })
    var TableInit = function () {
        var oTableInit = new Object();
        //初始化Table
        oTableInit.Init = function () {
            $('#group_show').bootstrapTable({
                url: '/disk/groupinfo/',         //请求后台的URL（*）
                method: 'get',    //请求方式（*）
                toolbar: '#toolbar',                //工具按钮用哪个容器
                striped: true,                      //是否显示行间隔色
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
                buttonsAlign: "left",
                singleSelect: true,
                columns: [{
                    checkbox: true
                }, {
                    field: 'group_name',
                    title: '群组名称',
                }, {
                    field: 'user_name',
                    title: '创建用户',
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
})





