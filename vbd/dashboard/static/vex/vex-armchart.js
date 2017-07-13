//曲线图
//chart_id: 图表的html ID. chart_data, 数据提供.
//graph_category_field是横轴读取数据的key, graph_category_axis_title是横轴显示的title
//graph_value_field是纵轴读取数据的key
//graph_balloon_title是滑动时显示数据的title
function drawLineChart(chart_id, chart_data, graph_category_field, graph_category_axis_title, graph_value_field, graph_balloon_title){
		AmCharts.makeChart(chart_id, {
		  "dataProvider": chart_data,
		  "type": "serial",
		  "theme": "light",
		  "marginRight": 10,
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