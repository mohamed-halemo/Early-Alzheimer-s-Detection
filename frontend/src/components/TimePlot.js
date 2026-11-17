import React, { useState,useEffect } from 'react';
import axios from "axios";
import serverConfig from '../server_config.json';

import CanvasJSReact from './canvasjs.react';
import { wait } from '@testing-library/user-event/dist/utils';
var CanvasJS = CanvasJSReact.CanvasJS;
var CanvasJSChart = CanvasJSReact.CanvasJSChart;
function TimePlot({Id}) {
	const [AD, setAD] = useState([]);
	const [CN, setCN] = useState([]);
	const [MCI, setMCI] = useState([]);
	const [predictedclass, setpredictedclass] = useState(null);

	const [vtk, setVtk] = useState(null);
  
	useEffect(() => {
  
	  (async function(){
		try {
		  let response = '';
		//  await axios.get(serverConfig.server_url+"images/predict/"+Id)
			// wait(1000);
		  response = await axios.get(serverConfig.server_url+"images/studies/"+Id)
		  console.log("RRRRRRR",response)
		  for (let j = 0; j < response.data.length; j++) {
			AD.push({ x: new Date(response.data[j].date_created), y: response.data[j].AD_percent  })
			CN.push({ x: new Date(response.data[j].date_created), y:  response.data[j].CN_percent  })
			MCI.push({ x: new Date (response.data[j].date_created) , y:  response.data[j].MCI_percent })		
		}
		
		  setAD(AD)
		  setCN(CN)
		  setMCI(MCI)
		  return (response);
		} catch (error) {
		  console.log(error)
		}
	  })()
	},[vtk])
	useEffect(() => {

	},[AD])
  
		var options = {
			  theme: "dark2",
              width: 340,
              height: 300,        
              backgroundColor:'#073D64',  
			  animationEnabled: true,
			  exportEnabled: true,
            title: {
                text: "Patient Progression",
                fontSize:15,
                verticalAlign:"top",
                fontfamily: "sans-serif",
                },

			  axisY: {
				title: "Class Percentage",
                margin:20,

			  },
			  toolTip: {
				shared: true
			  },
			  legend: {
				verticalAlign: "center",
				horizontalAlign: "right",
				reversed: true,
				cursor: "pointer",
				// itemclick: this.toggleDataSeries
			  },
			//   axisY: {
			// 	prefix: "₹"
			// },
			
			data: [
			{
				type: "area",
				name: "MCI",
				showInLegend: true,
				xValueFormatString: "MMM YYYY",
				// percentFormatString: "#0.##",

				yValueFormatString: "#,##0.0\"%\"",
				// dataPoints: [
				// 	// { x: new Date("2017- 01- 01"), y: 67.515},
				// 	// { x: new Date("2017- 02- 01"), y: 66.725},
				// 	// { x: new Date("2017- 03- 01"), y: 64.86},
				// 	// { x: new Date("2017- 04- 01"), y: 64.29},
				// 	// { x: new Date("2017- 05- 01"), y: 64.51},
				// 	// { x: new Date("2017- 06- 01"), y: 64.62},
				// 	// { x: new Date("2017- 07- 01"), y: 64.2},
				// 	// { x: new Date("2017- 08- 01"), y: 63.935},
				// 	// { x: new Date("2017- 09- 01"), y: 65.31},
				// 	// { x: new Date("2017- 10- 01"), y: 64.75},
				// 	// { x: new Date("2017- 11- 01"), y: 64.49},
				// 	{ x: new Date("2023-05-22T12:33:54.757932Z"), y: 63.84}
				// ]
				dataPoints:MCI
			},
			{
				type: "area",
				name: "AD",
				showInLegend: true,
				xValueFormatString: "MMM YYYY",

				yValueFormatString: "#,##0.0\"%\"",
				// dataPoints: [
				// 	// { x: new Date("2017- 01- 01"), y: 84.927},
				// 	// { x: new Date("2017- 02- 01"), y: 82.609},
				// 	// { x: new Date("2017- 03- 01"), y: 81.428},
				// 	// { x: new Date("2017- 04- 01"), y: 83.259},
				// 	// { x: new Date("2017- 05- 01"), y: 83.153},
				// 	// { x: new Date("2017- 06- 01"), y: 84.180},
				// 	// { x: new Date("2017- 07- 01"), y: 84.840},
				// 	// { x: new Date("2017- 08- 01"), y: 82.671},
				// 	// { x: new Date("2017- 09- 01"), y: 87.496},
				// 	// { x: new Date("2017- 10- 01"), y: 86.007},
				// 	// { x: new Date("2017- 11- 01"), y: 87.233},
				// 	{ x: new Date("2023-05-22T12:33:54.757932Z"), y: 86.276}
				// ]
				dataPoints: AD
			},
			
			{
				type: "area",
				name: "CN",
				showInLegend: true,
				xValueFormatString: "MMM YYYY",
				yValueFormatString: "#,##0.0\"%\"",
				// dataPoints: [
				// 	// { x: new Date("2017- 01- 01"), y: 67.515},
				// 	// { x: new Date("2017- 02- 01"), y: 66.725},
				// 	// { x: new Date("2017- 03- 01"), y: 64.86},
				// 	// { x: new Date("2017- 04- 01"), y: 64.29},
				// 	// { x: new Date("2017- 05- 01"), y: 64.51},
				// 	// { x: new Date("2017- 06- 01"), y: 64.62},
				// 	// { x: new Date("2017- 07- 01"), y: 64.2},
				// 	// { x: new Date("2017- 08- 01"), y: 63.935},
				// 	// { x: new Date("2017- 09- 01"), y: 65.31},
				// 	// { x: new Date("2017- 10- 01"), y: 64.75},
				// 	// { x: new Date("2017- 11- 01"), y: 64.49},
				// 	{ x: new Date("2023-05-22T12:33:54.757932Z"), y: 63.84}
				// ]
				dataPoints:CN
			}

			]
		}
		return (
		<div>
			<CanvasJSChart options = {options}			/>
			{/*You can get reference to the chart instance as shown above using onRef. This allows you to access all chart properties and methods*/}
		</div>
		);
	}
export default TimePlot;