document.getElementById("todayAmmount").textContent = jsObjectToday.todayAmmount;
document.getElementById("todayDatetime").textContent = jsObjectToday.todayDatetime;
document.getElementById("todayAverage").textContent = jsObjectToday.todayAverage;
document.getElementById("todayHighest").textContent = jsObjectToday.todayHighest;
document.getElementById("todayLowest").textContent = jsObjectToday.todayLowest;
document.getElementById("todayConstant").textContent = jsObjectToday.todayConstant;

var today = new Date();

var todayDate = today.toLocaleString('en-US', {hour12:false});
var todayUTCDate = today.toLocaleString('en-US', {hour12:false,timeZone:'UTC'});
var hoursDiff = today.getTimezoneOffset() / 60;

document.getElementById("todayDate").textContent = todayDate;
document.getElementById("todayUTCDate").textContent = todayUTCDate;
document.getElementById("hoursDiff").textContent = hoursDiff;




var lastBtnTapped = null;

google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

window.addEventListener("orientationchange", function() {
	setTimeout(function(){
					if(lastBtnTapped != null) {
						document.getElementById(lastBtnTapped).click()
					}
					else {
						google.charts.load('current', {'packages':['corechart']});
						google.charts.setOnLoadCallback(drawChart);
					}
	}, 250);

}, false);



function drawChart() {

	var data = new google.visualization.DataTable();

	data.addColumn('date', 'Date');
	data.addColumn('number', 'Average');
	data.addColumn('number', 'Highest');
	data.addColumn('number', 'Lowest');

	for (i = 0, len = jsArrayPerDay.length; i < len; i++) {
		data.addRow([ new Date(jsArrayPerDay[i][0]), parseFloat(jsArrayPerDay[i][1]), parseFloat(jsArrayPerDay[i][2]), parseFloat(jsArrayPerDay[i][3]) ]);
	}
	
	var minArrayPerDay = 0;
	var maxArrayPerDay = jsArrayPerDay.length-1;

	var options = {
		title: 'R3m1tly: Rate exchange from USD to MXN per day.',
		legend: { position: 'bottom' },
		//~ width: 900,
		//~ height: 500,
		height: 400,
		orientation: 'horizontal',
		is3D: true,
		colors: ['#1a8cff', '#009900', '#cc0000'],
		series: {
			0: {axis: 'average', lineWidth: 3, targetAxisIndex:1},
			1: {axis: 'highest', lineWidth: 1, lineDashStyle: [14, 2, 7, 2], targetAxisIndex:1},
			2: {axis: 'lowest', lineWidth: 1, lineDashStyle: [14, 2, 7, 2], targetAxisIndex:1},
		},
		vAxis: {
			title: 'MXN / USD',
			format: 'currency',
		},
		hAxis: {
			title: 'UTC: DATE TIME',
			format: 'MMM/dd',
			gridlines: { count: jsArrayPerDay.length },
			viewWindow: {
				min: jsArrayPerDay[minArrayPerDay][0],
				max: jsArrayPerDay[maxArrayPerDay][0],
			},
		},
	};

	var chart = new google.visualization.LineChart(document.getElementById('chartsPerDay'));


	chart.draw(data, options);

	var allButtonsFilter = Array(7,15,30,60,90,180,365);

	for (var a=0; a < allButtonsFilter.length; a++) {
		if (document.getElementById('last'+allButtonsFilter[a]+'Days')) {
			document.getElementById('last'+allButtonsFilter[a]+'Days').style.color = 'initial';
		}
	}

	if (document.getElementById('last7Days')) buttonFilterClick(7);

	if (document.getElementById('last15Days')) buttonFilterClick(15);

	if (document.getElementById('last30Days')) buttonFilterClick(30);

	if (document.getElementById('last60Days')) buttonFilterClick(60);

	if (document.getElementById('last90Days')) buttonFilterClick(90);

	if (document.getElementById('last180Days')) buttonFilterClick(180);

	if (document.getElementById('last365Days')) buttonFilterClick(365);


	if (document.getElementById('lastAllDays')) {

		document.getElementById('lastAllDays').style.color = 'blue';

		document.getElementById('lastAllDays').onclick = function () {
			options.hAxis.viewWindow.min = jsArrayPerDay[minArrayPerDay][0];
			options.hAxis.viewWindow.max = jsArrayPerDay[maxArrayPerDay][0];
			chart.draw(data, options);
			for (var a=0; a < allButtonsFilter.length; a++) {
				if (document.getElementById('last'+allButtonsFilter[a]+'Days')) {
					document.getElementById('last'+allButtonsFilter[a]+'Days').style.color = 'initial';
				}
			}
			this.style.color = 'blue';
			lastBtnTapped = 'lastAllDays';
		};
	}


	function buttonFilterClick(daysFilter) {
		
		document.getElementById('last'+daysFilter+'Days').onclick = function () {

			var minArrayPerDayFilter = maxArrayPerDay - daysFilter;

			if (minArrayPerDayFilter < 0) minArrayPerDayFilter = 0;

			options.hAxis.viewWindow.min = jsArrayPerDay[minArrayPerDayFilter][0];
			options.hAxis.viewWindow.max = jsArrayPerDay[maxArrayPerDay][0];
			chart.draw(data, options);
			
			if (document.getElementById('lastAllDays')) document.getElementById('lastAllDays').style.color = 'initial';

			for (var a=0; a < allButtonsFilter.length; a++) {
				if (document.getElementById('last'+allButtonsFilter[a]+'Days')) {
					document.getElementById('last'+allButtonsFilter[a]+'Days').style.color = 'initial';
				}
			}

			this.style.color = 'blue';
			lastBtnTapped = 'last'+daysFilter+'Days';

		};
	}
}



