/**
 * Created by dalin on 16-5-20.
 */

$(document).ready(function(){

  $.fn.echart = function(){
    $(this).each(function(){
      var $slice = $(this);
      var slice_url = $slice.data('slice-url');
      var slice_id = $slice.attr('id');
      var myChart = echarts.init(document.getElementById(slice_id),'shine');
      $.getJSON(slice_url,{'all':''}, function(data){
        myChart.setOption(data);
      });
    })
  }

  $('.slice').echart();
});
