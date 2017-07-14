/**
 * 柱状图
 * @param chart_id: chart div 的ID
 * @param chart_data: chart数据提供
 * @param graph_category_field: chart显示的title, 其值为chart_data[0].graph_category_field
 * @param graph_value_field_1: 柱状图上部分数值, 其值为chart_data[0].graph_value_field_1
 * @param graph_value_field_2: 柱状图下部分数值, 其值为chart_data[0].graph_value_field_2
 * @returns
 * chartData = [ {
	  "category": "Wine left in the barrel",
	  "value1": 30,
	  "value2": 70
	} ];	
	drawCylinderGaugeChart("memoryChart", memory_chartData, "category", "value1", "value2");
*/
function drawCylinderGaugeChart(chart_id, chart_data, graph_category_field, graph_value_field_1, graph_value_field_2){
	var chart = AmCharts.makeChart(chart_id, {
		  "theme": "none",
		  "type": "serial",
		  "depth3D": 100,
		  "angle": 30,
		  "autoMargins": false,
		  "marginBottom": 40,
		  "marginTop": 10,
		  "marginLeft": 80,
		  "marginRight": 10,
		  "dataProvider": chart_data,
		  "valueAxes": [ {
		    "stackType": "100%",
		    "gridAlpha": 0
		  } ],
		  "graphs": [ {
		    "type": "column",
		    "topRadius": 1,
		    "columnWidth": 1,
		    "showOnAxis": true,
		    "lineThickness": 5,
		    "lineAlpha": 0.9,
		    "lineColor": "#FFFFFF",
		    "fillColors": "#8d003b",
		    "fillAlphas": 0.9,
		    "valueField": graph_value_field_1
		  }, {
		    "type": "column",
		    "topRadius": 1,
		    "columnWidth": 1,
		    "showOnAxis": true,
		    "lineThickness": 2,
		    "lineAlpha": 0.5,
		    "lineColor": "#cdcdcd",
		    "fillColors": "#cdcdcd",
		    "fillAlphas": 0.5,
		    "valueField": graph_value_field_2
		  } ],

		  "categoryField": graph_category_field,
		  "categoryAxis": {
		    "axisAlpha": 0,
		    "labelOffset": 40,
		    "gridAlpha": 0,
		  },
		  "export": {
		    "enabled": false
		  }
		} );
	return chart;
}

/**
 * 柱状图
 * @param chart_id: chart div 的ID
 * @param chart_data: chart数据提供
 * @param graph_category_field: chart横轴数据, 其值为chart_data[0].graph_category_field
 * @param graph_value_field: chart纵轴数据, 其值为chart_data[0].graph_value_field
 * @param graph_balloon_title: 滑动时显示数据的title
 * @returns
	var chartData = [{
        "date": "Thu Jul 13 2017 00:33:17 GMT+0800 (CST)",
        "value": 13
    }, {
        "date": "Thu Jul 13 2017 00:34:17 GMT+0800 (CST)",
        "value": 11
    }];
	
	drawLineChart("cpuChart", chartData, "date", "Cpu Usage", "value", "Usage");
*/
function drawLineChart(chart_id, chart_data, graph_category_field, graph_category_axis_title, graph_value_field, graph_balloon_title){
		AmCharts.makeChart(chart_id, {
		  "dataProvider": chart_data,
		  "type": "serial",
		  "theme": "light",
		  "marginRight": 20,
		  "marginTop": 10,
		  "marginLeft": 20,
		  "autoMarginOffset": 5,
		  "valueAxes": [{
			"id": "v1",
			"axisAlpha": 0,
		    "position": "left",
		    "ignoreAxisWidth": false,
		    "title": graph_category_axis_title
		  }],
		  "balloon": {
		    "borderThickness": 1,
		    "shadowAlpha": 0
		  },
		  "graphs": [{
		    "id": "g1",
		    "balloon": {
		        "drop": true,
		        "adjustBorderColor": false,
		        "color": "#ffffff",
		        "type": "smoothedLine"
		      },
		    "fillAlphas": 0.4,
		    "bullet": "round",
		    "bulletBorderAlpha": 1,
		    "bulletColor": "#FFFFFF",
		    "bulletSize": 1,
		    "hideBulletsCount": 50,
		    "lineThickness": 2,
		    "title": "red line",
		    "useLineColorForBulletBorder": true,
		    "valueField": graph_value_field,
		    "balloonText": "<div style='margin:1px; font-size:12px;'>" + graph_balloon_title +": <b>[[value]]</b></div>"
		  }],
		  "chartCursor": {
		    "categoryBalloonDateFormat": "JJ:NN, DD MMMM",
		    "cursorPosition": "mouse",
		    "valueLineEnabled": true,
		    "valueLineBalloonEnabled": true,
		    "cursorAlpha": 0,
		    "zoomable": false,
		    "valueZoomable": true,
		    "valueLineAlpha": 0.5,
		    "selectWithoutZooming": true,
		  },
		  "categoryField": graph_category_field,
		  "categoryAxis": {
		    "minPeriod": "mm",
		    "parseDates": true,
		    "dashLength": 1,
		    "minorGridEnabled": true
		  }
		});
	}


//柱状图
//chart_id: 图表的html ID. chart_data, 数据提供.
//graph_category_field是横轴读取数据的key, graph_category_axis_title是横轴显示的title
//graph_value_field是纵轴读取数据的key, graph_value_axis_title是纵轴显示的title
//graph_color_field是横轴读取color数据的key
function drawColumnBarAmCharts(chart_id, chart_data, graph_category_field, graph_category_axis_title, graph_value_field, graph_value_axis_title, graph_color_field){
	var chart = AmCharts.makeChart(chart_id, {
  		"type": "serial",
  		"theme": "light",
  		"marginRight": 10,
  		"dataProvider": chart_data,
  		"valueAxes": [{
		    "axisAlpha": 1,
		    "position": "left",
		    "title": graph_value_axis_title
		}],
  		"graphs": [{
    		"balloonText": "<b>[[category]]: [[value]]</b>",
    		"fillColorsField": graph_color_field,
    		"fillAlphas": 0.9,
    		"lineAlpha": 0.1,
    		"type": "column",
    		"valueField": graph_value_field,
  		}],
  		"chartCursor": {
    		"categoryBalloonEnabled": false,
    		"cursorAlpha": 0,
    		"zoomable": false
  		},
  		"categoryField": graph_category_field,
  		"categoryAxis": {
    		"gridPosition": "start",
    		"labelRotation": 45,
    		"title":graph_category_axis_title
  		},
  		"export": {
    		"enabled": false
  		}
	});
}