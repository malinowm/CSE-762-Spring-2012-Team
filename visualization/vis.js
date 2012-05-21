var $win = $(window)
  , svg_width = $win.width() * .95
  , svg_height = $win.height() * .95;

var rectDemo = d3.select("#chart")
    .append("svg:svg")
    .attr("width", svg_width)
    .attr("height", svg_height)
    .on("click", function(){
      d3.select(this).selectAll(".detail").remove();
    });

$.getJSON("/scatterplot.json", function(r){
  //var total_points = gimme_random_total_points();
  r.data.slice(0, 10000).forEach(function(point){
    rectDemo.append("svg:circle")
            .attr("class", "point")
            .attr("r", 4)
            .attr("cx", (point.x) * svg_width)
            .attr("cy", svg_height-point.y * svg_height)
            .attr("pair", point.pair.join(','))
            .on("mouseover", function(e){
              rectDemo.selectAll(".detail").remove();
              d3.select(this).attr("r", 10).attr("class", "point hover");
              draw_scatter_plot_for(this);
              d3.event.preventDefault();
              d3.event.stopPropagation();
            })
            .on("mouseout", function(){
              d3.select(this).attr("r", 4).attr("class", "point");
            });
  });
});

function draw_scatter_plot_for(point){
  // using fake data to simulate AJAX call.
  var self = d3.select(point)
    , x = parseFloat(self.attr("cx"))
    , y = parseFloat(self.attr("cy"))
    , pair = self.attr("pair")
    , pairwise_width = 400
    , pairwise_height = 400
    , pairwise_points = gimme_random_pairwise_points();

    if((x + pairwise_width) > svg_width){
      x -= pairwise_width;
    }
    if(y + pairwise_height > svg_height){
      y -= pairwise_height;
    }
    
  var rect = rectDemo.append("svg:g")
              .attr("class", "detail")
              .attr("transform", "translate("+x+","+y+")")
              .attr("width", pairwise_width)
              .attr("height", pairwise_height);

  rect.append("svg:rect")
      .attr("x", 0)
      .attr("y", 0)
      .attr("width", pairwise_width)
      .attr("height", pairwise_height);

  pairwise_points.forEach(function(point){
    rect.append("svg:circle")
        .attr("class", "pairwise_point")
        .attr("cx", point.x)
        .attr("cy", pairwise_height - point.y)
        .attr("r", 3);
  });
}

function gimme_random_total_points(){
  var points = []
    , random_gen = d3.random.normal(0, svg_height/3)
    , pairs = pairs_gen();

  for(var i=0, l = pairs.length; i<l; i++){
    points.push({x: Math.abs(random_gen()), y: Math.abs(random_gen()), pair: pairs[i]});
  }
  return points;
}

function gimme_random_pairwise_points(){
  var points = []
    , random_gen = d3.random.normal(5, 400/4);

  for(var i=0, l = 100; i<l; i++){
    points.push({x: Math.abs(random_gen()), y: Math.abs(random_gen())});
  }
  return points;
}

function pairs_gen(){
  // generates pairs, [(a,a),(a,b),...,(Z,Z)]
  var p = [[97, 97+26], [65, 65+26]]
    , chars = [];
  for(var l=0; l<p.length; l++){
    var n = p[l][0], m = p[l][1];
    for(var i=n; i<m; i++){
      chars.push(String.fromCharCode(i));
    }
  }
  return generateCombinations(chars, 2);
}

// modified code from http://david-burger.blogspot.com/2008/09/generating-combinations-in-ruby-and_21.html
function generateCombinations(array, r) {
    function equal(a, b) {
        for (var i = 0; i < a.length; i++) {
            if (a[i] != b[i]) return false;
        }
        return true;
    }
    function values(i, a) {
        var ret = [];
        for (var j = 0; j < i.length; j++) ret.push(a[i[j]]);
        return ret;
    }
    var result = [];
    var n = array.length;
    var indices = [];
    for (var i = 0; i < r; i++) indices.push(i);
    var final = [];
    for (var i = n - r; i < n; i++) final.push(i);
    while (!equal(indices, final)) {
        result.push(values(indices, array));
        var i = r - 1;
        while (indices[i] == n - r + i) i -= 1;
        indices[i] += 1;
        for (var j = i + 1; j < r; j++) indices[j] = indices[i] + j - i;
    }
    result.push(values(indices, array));
    return result;
}
