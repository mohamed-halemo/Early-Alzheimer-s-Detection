import React, { useState,useEffect } from 'react';
import axios from "axios";
import serverConfig from '../server_config.json';
import CanvasJSReact from './canvasjs.react';
import TimePlot from './TimePlot';

var CanvasJS = CanvasJSReact.CanvasJS;
var CanvasJSChart = CanvasJSReact.CanvasJSChart;
function Pie_chart({Id}) {
  const [AD, setAD] = useState(0);
  const [CN, setCN] = useState(0);
  const [MCI, setMCI] = useState(0);
  const [predicted, setpredicted] = useState(null);
  const [vtk, setVtk] = useState(null);

  useEffect(() => {

    (async function(){
      try {
        let response = '';
  
        response = await axios.get(serverConfig.server_url+"images/predict/"+Id)
        setAD(response.data["AD_percent"])
        setCN(response.data["CN_percent"])
        setMCI(response.data["MCI_percent"])
        setpredicted(response.data["predicted_class"])

        return (response);
      } catch (error) {
        console.log(error)
      }
    })()
  },[vtk])

  const options = {
    theme: "dark2",
    backgroundColor:' #073D64',
    width: 340,
    height: 305,
    horizontalAlign: 'left',
    animationEnabled: true,
    // title: {
    //   text: "Patient Prediction",
    //   fontSize:15,
    //   verticalAlign:"top",
    //   fontfamily: "sans-serif",
    // },
    subtitles: [{
      text: predicted,
      verticalAlign: "center",
      fontSize: 40,
      dockInsidePlotArea: true
    }],
    data: [{
     
      type: "doughnut",
      showInLegend: true,
      indexLabel: "{name}: {y}",
      yValueFormatString: "#.##'%'",
      radius: "78%", 
      indexLabelPlacement:"outside",
      dataPoints: [
        { name: "MCI", y: MCI },
        { name: "AD", y: AD },
        { name: "CN", y: CN }
      ]
    }]
  }

  return (
    <div>
    <CanvasJSChart options = {options}
      /* onRef={ref => this.chart = ref} */
    />
    {/*You can get reference to the chart instance as shown above using onRef. This allows you to access all chart properties and methods*/}
    <div  className="timeplot">
    { predicted !=null && <TimePlot Id={Id}/>}
    </div>
  </div>
  
  );
}

export default Pie_chart;