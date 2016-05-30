$(document).ready(function(){
			$(':submit.btn-primary').click(function(){
				var jsonData = {};
				var titleShow = document.getElementById('id_step_2-title_show').checked;
				var title = {};
				title.show = titleShow;
				jsonData.title = title;
				var legendShow = document.getElementById('id_step_2-legend_show').checked;
				var legend = {};
				legend.show = legendShow;
				jsonData.legend = legend;
				var tooltipShow = document.getElementById('id_step_2-tooltip_show').checked;
				var tooltip = {};
				tooltip.show = tooltipShow;
				jsonData.tooltip = tooltip;
				var toolboxShow = document.getElementById('id_step_2-toolbox_show').checked;
				var toolbox = {};
				toolbox.show = toolboxShow;
				jsonData.toolbox = toolbox;
				var gridShow = document.getElementById('id_step_2-grid_show').checked;
				var grid = {};
				grid.show = gridShow;
				jsonData.grid = grid;
				var xAxisTypeVal = $('#id_step_2-xAxis_type').val().trim();
				var xAxis = {};
				//xAxis.type = xAxisVal;
				//jsonData.xAxis = xAxis;
				var xAxisData = new Array();
				$("div[name='step_2-xAxis']").each(function(index,value){
        			xAxisData[index]={};
        			xAxisData[index].type=$(value).find("select[name='step_2-xAxis-type']").val().trim();
        			xAxisData[index].value=$(value).find("input[name='step_2-xAxis-index']").val().trim();
        			xAxisData[index].dataName=$(value).find("input[name='step_2-xAxis-name']").val().trim();
    			});
    			xAxis.data = xAxisData;
    			xAxis.type = xAxisTypeVal;
    			jsonData.xAxis = xAxis;
    			var series = {};
    			var seriesData = new Array();
				$("div[name='step_2-series']").each(function(index,value){
        			seriesData[index]={};
        			seriesData[index].type=$(value).find("select[name='step_2-series-type']").val().trim();
        			seriesData[index].value=$(value).find("input[name='step_2-series-index']").val().trim();
        			seriesData[index].dataName=$(value).find("input[name='step_2-series-name']").val().trim();
    			});
    			series.data = seriesData;
    			//series.type = xAxisTypeVal;
    			jsonData.series = series;
				console.log(JSON.stringify(jsonData));
			});
});
/*
{
  "yAxis": {"type": "value"},
  "series": [
    {
        "type": "line",
        "name": "当日PV",
        "data": {"type": "column_name","value":"pv_all_1"}
    },
    {
        "data": {"type": "column_name", "value":"pv_all_2"},
        "type": "line",
        "name": "对比日PV"
    }
  ],
  "tooltip": {"trigger": "axis"},
  "title":{
  	   "show": "true",
  	   "text":"This is a test"
	},
  "grid": {"right": "4%", "bottom": "3%", "containLabel": "true", "left": "3%"},
  "xAxis": {
       "data": {"type":"column_name", "value":"f_time"},
       "type": "category",
       "boundaryGap": "false"
   },
  "toolbox": {"feature": {"saveAsImage": {}}},
  "legend": {"data": ["当日PV", "对比日PV"]}
}



*/