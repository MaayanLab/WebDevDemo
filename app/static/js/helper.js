var url = "/webdevdemo/api/enrichment"

var radio_listener = () => {
	var radios = document.forms["library-radio"].elements["library"];
	for(var i = 0, max = radios.length; i < max; i++) {
		radios[i].onclick = function() {
			update_data()
		}
	}
};

var update_data = () => {
	var library = document.querySelector('input[name="library"]:checked').value
	var signature = document.querySelector('input[name="autocomplete"]').value
	if (signature !== "") {
		console.log(library, signature)
		// update(library, signature)
		fetch(`${url}?signature=${signature}&library=${library}`)
			.then(response => response.json())
		  	.then(data => {
			  update(data)
		  	})
	}
}



// adapted from https://www.d3-graph-gallery.com/graph/barplot_button_data_csv.html
// set the dimensions and margins of the graph
var margin = {top: 20, right: 30, bottom: 40, left: 50},
	width = 460 - margin.left - margin.right,
	height = 400 - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg = d3.select("#my-plot")
.append("svg")
	.attr("width", width + margin.left + margin.right)
	.attr("height", height + margin.top + margin.bottom)
.append("g")
	.attr("transform",
		"translate(" + margin.left + "," + margin.top + ")");

// Initialize the X axis
var x = d3.scaleLinear()
	.range([ 0, width ])
var xAxis = svg.append("g")
	.attr("transform", "translate(0," + height + ")")

// Initialize the Y axis
// var y = d3.scaleLinear()
// 	.range([ height, 0]);
var y = d3.scaleBand()
	.range([ 0, height])
	.padding(.1);

var yAxis = svg.append("g")
	.attr("class", "myYaxis")
	


function update(data) {
	// X axis
	x.domain([0, d3.max(data, function(d) { return d['-log pval'] }) ]);
	xAxis.transition().duration(1000)

	// Add Y axis
	y.domain(data.map(function(d) { return d.label; }))
	yAxis.transition().duration(1000);
	
	// variable u: map data to existing bars
	var u = svg.selectAll("rect")
		.data(data)

	// update bars
	u.enter()
	 .append("rect")
	 .merge(u)
	 .transition()
	 .duration(1000)
	 .attr("x", x(0))
	 .attr("y", function(d) { return y(d.label); })
	 .attr("width", function(d) { return x(d['-log pval']); })
	 .attr("height", y.bandwidth())
	 .attr("fill", "#69b3a2")

	var t = svg.selectAll(".bar-labels")
	 .data(data)

	// update bars
	t.enter()
	.append("text")
	.merge(t)
	.attr("x", x(0) + 5)
	.attr("y", function(d) { return y(d.label) + 10; })
	.text(function(d) { return d.label; })
	.attr("fill", "black")
	.attr("font-size", "10")
	.attr("class", "bar-labels")
}