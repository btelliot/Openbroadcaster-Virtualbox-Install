// Configuration
const csvFile = 'listeners.csv';
const daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
const colors = ['#ffffb2', '#fed976', '#feb24c', '#fd8d3c', '#fc4e2a', '#e31a1c', '#b10026'];

let globalData; // Declare a global variable to hold the data
let globalSummaryData;

// Read data from the CSV file
d3.csv(csvFile).then(data => {
  globalData = data; // Assign the parsed data to the global variable
  globalSummaryData = summarizeData(data);
  const summaryData = summarizeData(data);
  renderHeatmap(summaryData);
  renderSummaryTable(summaryData);
});


// Calculate Average Listeners for days of the week and hours of the day
function summarizeDataAvg(data) {
  const listenerCounts = new Array(7).fill(0).map(() => new Array(24).fill(0));
  const dataPointCounts = new Array(7).fill(0).map(() => new Array(24).fill(0));

  data.forEach(row => {
    const timestamp = new Date(row.Timestamp);
    const day = timestamp.getDay();
    const hour = timestamp.getHours();
    const listeners = parseInt(row.ListenerPeak, 10);

    listenerCounts[day][hour] += listeners;
    dataPointCounts[day][hour] += 1;
  });

  const summaryData = listenerCounts.map((dayRow, dayIndex) =>
    dayRow.map((listenerCount, hourIndex) => {
      const dataPoints = dataPointCounts[dayIndex][hourIndex];
      return Math.round(dataPoints === 0 ? 0 : listenerCount / dataPoints);
    })
  );

  return summaryData;
}

//calculatePeakListeners for days of the week and hours of the day
function summarizeData(data) {
  // Initialize the summary data structure
  const summaryData = Array(7).fill().map(() => Array(24).fill(0));

  data.forEach(row => {
    // Check if the ListenersPeak value is not null
    if (row.Listeners!== null) {
      const date = new Date(row.Timestamp);
      const day = (date.getDay()); 
      const hour = date.getHours();

      // Store the maximum ListenersPeak value for each day and hour
      if (row.Listeners> summaryData[day][hour]) {
        summaryData[day][hour] = row.Listeners-3;
      }
    }
  });

  return summaryData;
}


// Render the heatmap
function renderHeatmap(summaryData) {
  const maxListeners = Math.max(...summaryData.map(row => Math.max(...row)));
  const table = d3.select('#heatmap').append('table').attr('class', 'heatmap');
  const thead = table.append('thead');
  const tbody = table.append('tbody');

  // Create tooltip element
  const tooltip = d3.select('body').append('div')
    .attr('class', 'tooltip')
    .style('opacity', 0);

  thead.append('tr')
    .selectAll('th')
    .data([''].concat(daysOfWeek))
    .enter()
    .append('th')
    .text(d => d);

  tbody.selectAll('tr')
    .data(summaryData[0].map((_, i) => i))
    .enter()
    .append('tr')
    .each(function (hour) {
      d3.select(this).selectAll('td')
        .data([hour].concat(summaryData.map(row => row[hour])))
        .enter()
        .append('td')
        .attr('class', (d, i) => (i === 0 ? 'hour-label' : ''))
        .style('background-color', (d, i) => i === 0 ? 'transparent' : getColor(d, maxListeners))
        .text((d, i) => (i === 0 ? `${d}:00` : d))
        .on('mouseover', function (event, d) {
          if (event.target.className.baseVal !== 'hour-label') {
            tooltip.transition()
              .duration(200)
              .style('opacity', .9);
            tooltip.html(`Hour: ${event.target.parentNode.firstChild.textContent}<br/>Peak Listeners: ${d}`)
              .style('left', (event.pageX + 10) + 'px')
              .style('top', (event.pageY - 28) + 'px');
          }
        })
        .on('mouseout', function () {
          tooltip.transition()
            .duration(500)
            .style('opacity', 0);
        });
    });

  function getColor(value, maxValue) {
    const index = Math.floor((colors.length - 1) * (value / maxValue));
    return colors[index];
  }
}

// Render the summary table
function renderSummaryTable(summaryData) {
  const table = d3.select('#summary-table').append('table').attr('class', 'table table-bordered');
  const thead = table.append('thead');
  const tbody = table.append('tbody');

  thead.append('tr')
    .selectAll('th')
    .data(['Hour'].concat(daysOfWeek))
    .enter()
    .append('th')
    .text(d => d);

  tbody.selectAll('tr')
    .data(summaryData[0].map((_, i) => i))
    .enter()
    .append('tr')
    .each(function (hour) {
      d3.select(this).selectAll('td')
        .data([hour].concat(summaryData.map(row => row[hour])))
        .enter()
        .append('td')
        .text((d, i) => (i === 0 ? `${d}:00` : d)); 
    });
}