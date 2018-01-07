$(function(){

    console.log("hello world")

    $("google-chart").on("google-chart-ready",function(ev){
	console.log("CHART READY")
	console.log(ev)
	last_ev= ev
	chart = ev.originalEvent.detail.chart
	
	// this chart object allows method calls... ie
	sel= chart.getSelection()
	
    })
    $("google-chart").on("google-chart-select",function(ev){
	last_ev= ev
	chart = ev.originalEvent.detail.chart
	
	// this chart object allows method calls... ie
	sel= chart.getSelection()
	console.log(sel)

    })
})
