  // scatterchart
  var M = 7919 * 6607;
  var rnds = [];
  x0 = Math.floor(M / 2);
  for (var i = 0; i < 30300; ++i) {
    rnds[i] = x0/M  - 0.5;
    x0 = (x0 * x0) % M;
  }
  chartsData.scatterchart = {};
  chartsData.scatterchart.data = new google.visualization.DataTable();
  chartsData.scatterchart.data.addColumn('number', 'A');
  chartsData.scatterchart.data.addColumn('number', 'Male');
  chartsData.scatterchart.data.addColumn('number', 'Female');

  for (var i = 0; i < 100; ++i) {
    var x = 0;
    var y1 = 0;
    var y2 = 0;
    for (var j = 0; j < 100; ++j) {
      var a1 = rnds[100 * i + j*3 + 1];
      var a2 = -0.1 + a1 * 2 + rnds[100 * i + j*3 + 2];
      var a3 = 0.1 - a1 * 1.5 + rnds[100 * i + j*3 + 3];
      x = x + a1; y1 = y1 + a2; y2 = y2 + a3;
    }
    chartsData.scatterchart.data.addRow([Math.floor(x*100)/100, Math.floor(y1*100)/100, Math.floor(y2*100)/100]);
  }

  chartsData.scatterchart.chart = new google.visualization.ScatterChart(document.getElementById('scatterchart'));

  chartsData.scatterchart.options = {
    chartArea: {
      top: '10%'
    },
    pointSize: 2,
    legend: 'none'
  };