/**
 * Convert InfluxDB query results to Chart.js Time-series datasets
 * @param data - InfluxDB Query Results
 */
function influx_to_chartjs(data) {
    var out = []
    for (let i = 0; i < data.series.length; i++) {
        let series = data.series[i]
        let color = random_rgb()
        let dataset = {
            label: JSON.stringify(series.tags),
            fill: false,
            backgroundColor: color,
            borderColor: color,
            data: series.values.map(
                point => ({
                    t: point[0],
                    y: point[1]
                }))
        }
        out.push(dataset)
    }
    return out
}


/**
 * Generate a random rgb color
 */
function random_rgb() {
    return 'rgb(' +
        Math.floor(Math.random()*256) + ',' +
        Math.floor(Math.random()*256) + ',' +
        Math.floor(Math.random()*256) + ')'
}
