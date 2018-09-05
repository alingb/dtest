$(document).ready(function () {
    testId('web/get_info/cpu/', 'cpustat', 'CPUSTAT', 'cpu(%)');
    testId('web/get_info/mem/', 'memstat', "MEMSTAT", 'mem(%)');
    buttonClick();
    var LogoTable = new LogTableInit();
    LogoTable.Init();
    netID('netstat', "NETSTAT");
    setTimeout(function () {
		document.getElementById("server_id").click();
    },5);

    // test();
});

function testId(url, name, tilte, msg) {
	if(document.getElementById(name)){
		main(url, name, tilte, msg);
	}
}

function netID(name, tilte) {
	if(document.getElementById(name)){
		test(name, tilte);
	}
}

function main(url, name, tilte, msg){
   // $.getJSON('https://data.jianshukeji.com/jsonp?filename=json/new-intraday.json&callback=?', function (data) {
    $.getJSON(url, function (data) {
	// create the chart
	Highcharts.stockChart(name, {
		credits:{
			enabled:false,
		},
		title: {
			text: tilte
		},
		subtitle: {
			text: ''
		},
		// xAxis: {
		// 	breaks: [{ // Nights
		// 		from: Date.UTC(2012, 9, 6, 16),
		// 		to: Date.UTC(2012, 9, 7, 8),
		// 		repeat: 24 * 36e5
		// 	}, { // Weekends
		// 		from: Date.UTC(2012, 9, 7, 16),
		// 		to: Date.UTC(2012, 9, 10, 8),
		// 		repeat: 7 * 24 * 36e5
		// 	},{
		// 	}]
		// },
		rangeSelector : {
			buttons : [{
				type : 'second',
				count : 30,
				text : '30s'
			},{
				type : 'minute',
				count : 1,
				text : '1m'
			}, {
				type : 'hour',
				count : 1,
				text : '1h'
			}, {
				type : 'day',
				count : 1,
				text : '1D'
			}, {
				type : 'all',
				count : 1,
				text : 'All'
			}],
			selected : 1,
			inputEnabled : true
		},
		tooltip: {
			split: true
		},
		series : [{
			name : msg,
			type: 'area',
			data : data,
			gapSize: 5,
			tooltip: {
				valueDecimals: 2
			},
			fillColor : {
				linearGradient : {
					x1: 0,
					y1: 0,
					x2: 0,
					y2: 1
				},
				stops : [
					[0, Highcharts.getOptions().colors[0]],
					[1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
				]
			},
			threshold: null
		}]
	});
});
}

function test(name, tilte) {
    var seriesOptions = [];
	seriesCounter = 0;
    const names = [];
    $("input").each(function () {
    	if (this.id){
    		names.push(this.id)
		}
    });
    // names = ['MSFT', 'AAPL', 'GOOG'];

/**
     * Create the chart when all data is loaded
     * @returns {undefined}
     */
function testChart(title) {
	Highcharts.stockChart(name, {
		credits:{
			enabled:false,
		},
		title: {
			text: 'NETSTAT: ' + title.split('_')[0].toUpperCase()
		},
		subtitle: {
			text: ''
		},
		// xAxis: {
		// 	breaks: [{ // Nights
		// 		from: Date.UTC(2012, 9, 6, 16),
		// 		to: Date.UTC(2012, 9, 7, 8),
		// 		repeat: 24 * 36e5
		// 	}, { // Weekends
		// 		from: Date.UTC(2012, 9, 7, 16),
		// 		to: Date.UTC(2012, 9, 10, 8),
		// 		repeat: 7 * 24 * 36e5
		// 	},{
		// 	}]
		// },
		rangeSelector : {
			buttons : [{
				type : 'second',
				count : 30,
				text : '30s'
			},{
				type : 'minute',
				count : 1,
				text : '1m'
			}, {
				type : 'hour',
				count : 1,
				text : '1h'
			}, {
				type : 'day',
				count : 1,
				text : '1D'
			}, {
				type : 'all',
				count : 1,
				text : 'All'
			}],
			selected : 4,
			inputEnabled : true
		},
		tooltip: {
			split: true
		},
		series: seriesOptions
	});
}
function createChart() {
	Highcharts.stockChart('container1', {
	    		title: {
			text: 'CPU STATUS'
		},
		chart: {
			zoomType: null,
			// pinchType: null
		},
		rangeSelector: {
			selected: 4
		},
		yAxis: {
			labels: {
				formatter: function () {
					return (this.value > 0 ? ' + ' : '') + this.value + '%';
				}
			},
			plotLines: [{
				value: 0,
				width: 2,
				color: 'silver'
			}]
		},
		plotOptions: {
			series: {
				compare: 'percent',
				showInNavigator: false
			}
		},
		tooltip: {
			pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.change}%)<br/>',
			valueDecimals: 2,
			followTouchMove: false,
			split: true
		},
		series: seriesOptions
	});
}
$.each(names, function (i, name) {
	$.getJSON('/web/get_info/' + name.toLowerCase(),    function (data) {
		seriesOptions[i] = {
			name: name,
			data: data
		};
		// As we're loading the data asynchronously, we don't know what order it will arrive. So
		// we keep a counter and create the chart when all the data is loaded.
		seriesCounter += 1;
		if (seriesCounter === names.length) {
			// createChart();
			testChart(name);
		}
	});
});
}

var LogTableInit = function () {
    var LogoTableInit = {};
    //初始化Table
    LogoTableInit.Init = function () {
        $('#logstat').bootstrapTable({
            url: '/web/get_info/loginfo/',         //请求后台的URL（*）
            method: 'get',    //请求方式（*）
            toolbar: '#toolbar',                //工具按钮用哪个容器
            striped: true,                      //是否显示行间隔色
            cache: true,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
            pagination: true,                   //是否显示分页（*）
            sortable: true,                     //是否启用排序
            sortOrder: "asc",                   //排序方式
            queryParams: LogoTableInit.queryParams,//传递参数（*）
            sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
            pageNumber: 1,                       //初始化加载第一页，默认第一页
            pageSize: 10,                       //每页的记录行数（*）
            pageList: [10, 25, 50, 100],        //可供选择的每页的行数（*）
            // search: true,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
            // strictSearch: true,
            // showColumns: true,                  //是否显示所有的列
            // showRefresh: true,                  //是否显示刷新按钮
            // minimumCountColumns: 2,             //最少允许的列数
            // clickToSelect: true,                //是否启用点击选中行
            // // height: 500,                        //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
            // // uniqueId: "ID",                     //每一行的唯一标识，一般为主键列
            // showToggle: true,                    //是否显示详细视图和列表视图的切换按钮
            // cardView: false,                    //是否显示详细视图
            // detailView: false,                   //是否显示父子表
            columns: [{
                checkbox: true
            }, {
                field: 'id',
                title: 'Event ID',
                // visible: false
            }, {
                field: 'time',
                title: 'Time Stamp'
            }, {
                field: 'name',
                title: 'Sensor Name'
            }, {
                field: 'type',
                title: 'Sensor Type'
            }, {
                field: 'desc',
                title: 'Description',
            },],
        });
    };
    //得到查询的参数
    LogoTableInit.queryParams = function (params) {
        var temp = {   //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
            limit: params.limit,   //页面大小
            offset: params.offset,  //页码
        };
        return temp;
    };
    return LogoTableInit;
};

function buttonClick() {
	$("select#netname").change(function(){
       //var options=$("select#test option:selected"); //可以获取到选中的option
        var options=$(this).children("option:selected").val(); //也可以获取到选中的option
		window.location.href = options;
})
}


