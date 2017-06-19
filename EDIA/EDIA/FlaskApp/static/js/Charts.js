google.charts.load("current", { packages: ["corechart"] });
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
    var data = google.visualization.arrayToDataTable([
        ["Element", "Percentage", { role: "style" }],
        ["Smiles in sequence", 17, "#ff0000"],
        ["Total smiles", 81, "#ba4bff"],
        ["Eyes movement", 52, "#ba4bff"],
        ["Head movement", 84, "color: #ba4bff"]
    ]);

    var view = new google.visualization.DataView(data);
    view.setColumns([0, 1,
                     {
                         calc: "stringify",
                         sourceColumn: 1,
                         type: "string",
                         role: "annotation"
                     },
                     2]);

    var options = {
        title: "Diagnosis Details:",
        width: 1000,
        height: 400,
        bar: { groupWidth: "80%" },
        legend: { position: "none" },
    };

    var chart = new google.visualization.BarChart(document.getElementById("barchart_values"));
    chart.draw(view, options);
}