$(document).ready(function () {
    main();
    test();
});

function main(){
    $.getJSON('https://data.jianshukeji.com/jsonp?filename=json/new-intraday.json&callback=?', function (data) {
	// create the chart
	Highcharts.stockChart('container', {
		title: {
			text: 'CPU STATUS'
		},
		subtitle: {
			text: 'Using explicit breaks for nights and weekends'
		},
		xAxis: {
			breaks: [{ // Nights
				from: Date.UTC(2012, 9, 6, 16),
				to: Date.UTC(2012, 9, 7, 8),
				repeat: 24 * 36e5
			}, { // Weekends
				from: Date.UTC(2012, 9, 7, 16),
				to: Date.UTC(2012, 9, 10, 8),
				repeat: 7 * 24 * 36e5
			},{
			}]
		},
		rangeSelector : {
			buttons : [{
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
			name : 'cpu',
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

function test() {
    var seriesOptions = [],
	seriesCounter = 0,
	names = ['MSFT', 'AAPL', 'GOOG'];
/**
     * Create the chart when all data is loaded
     * @returns {undefined}
     */
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
	$.getJSON('https://data.jianshukeji.com/jsonp?filename=json/' + name.toLowerCase() + '-c.json&callback=?',    function (data) {
		seriesOptions[i] = {
			name: name,
			data: data
		};
		console.log('https://data.jianshukeji.com/jsonp?filename=json/' + name.toLowerCase() + '-c.json&callback=?');
		// As we're loading the data asynchronously, we don't know what order it will arrive. So
		// we keep a counter and create the chart when all the data is loaded.
		seriesCounter += 1;
		if (seriesCounter === names.length) {
			createChart();
		}
	});
});

}
