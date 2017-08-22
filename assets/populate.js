let ids = {
  '197162': 'cycling',
  '2298': 'running',
};

let chartData = {
  'keys': [],
  'cycling': [],
  'running': []
};

function setupText(json, lookup) {
  let latest = false;
  for (let key in json) {
    if (!latest) {
      let distance = document.getElementById(`${lookup}-distance`);
      distance.textContent = Math.round(json[key].distance / 1000);
      let athletes = document.getElementById(`${lookup}-athletes`);
      athletes.textContent = json[key].athletes;
      latest = true;
    }
  }
}

function collectData(json, lookup) {
  for (let key in json) {
    chartData[lookup].push(parseInt(json[key].distance / 1000));
  }
  if (chartData.cycling.length > 0 && chartData.running.length > 0) {
    chartData['keys'] = Object.keys(json);
    showGraph();
  }
}

function showGraph() {
  let element = document.getElementById(`chart`).getContext("2d");
  let options = {};
  let chart = new Chart(element, {
    type: 'bar',
    data: {
      labels: chartData['keys'].slice(0, 5).reverse(),
      datasets: [
      {
        label: 'Running',
        data: chartData['running'].slice(0, 5).reverse(),
        fill: false,
        backgroundColor: 'blue',
        borderColor: 'blue',
      },
      {
        label: 'Cycling',
        data: chartData['cycling'].slice(0, 5).reverse(),
        fill: false,
        backgroundColor: 'firebrick',
        borderColor: 'firebrick',
      }
      ]
    },
    options: {
      responsive: true,
      scales: {
          xAxes: [{
              display: true,
              scaleLabel: {
                  display: true,
                  labelString: 'Date'
              }
          }],
          yAxes: [{
              display: true,
              scaleLabel: {
                  display: true,
                  labelString: 'KM'
              },
              beginAtZero: true,
          }]
      }
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  for (let id in ids) {
    let lookup = ids[id];
    fetch(`summaries/summary.${id}.json`)
    .then((response) => {
      return response.json();
    }).then((json) => {
      setupText(json, lookup);
      collectData(json, lookup);
    });
  }
});
