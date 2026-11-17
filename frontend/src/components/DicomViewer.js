import React, { useEffect, useRef, useState } from "react";
import dicomParser from "dicom-parser";
import cornerstone from "cornerstone-core";
import cornerstoneWADOImageLoader from "cornerstone-wado-image-loader";
import cornerstoneMath from "cornerstone-math";
import OpenInBrowserIcon from '@mui/icons-material/OpenInBrowser';
import ClearIcon from '@mui/icons-material/Clear';
import StraightenIcon from '@mui/icons-material/Straighten';
import ZoomInIcon from '@mui/icons-material/ZoomIn';
import Crop169Icon from '@mui/icons-material/Crop169';
import PanoramaFishEyeIcon from '@mui/icons-material/PanoramaFishEye';
import TextRotationAngleupIcon from '@mui/icons-material/TextRotationAngleup';
import CheckBoxOutlineBlankIcon from '@mui/icons-material/CheckBoxOutlineBlank';
import GetAppIcon from '@mui/icons-material/GetApp';
import HistoryIcon from '@mui/icons-material/History';
import LoopIcon from '@mui/icons-material/Loop';
import PanToolIcon from '@mui/icons-material/PanTool';
import cornerstoneTools from "cornerstone-tools";
import Hammer from "hammerjs";
import "./../styles/styles.scss";
import Pie_chart from './Pie_chart';
import TimePlot from './TimePlot';
import { useNavigate } from 'react-router-dom';
import Slider from '@mui/material/Slider';
import axios from "axios";
import serverConfig from '../server_config.json';

import { ZoomTool, LengthTool ,RectangleRoiTool,EllipticalRoiTool,PanTool,AngleTool,FreehandRoiTool,RotateTool} from "cornerstone-tools";
import { initLocalFileLoader } from "./Visualization3D_old";
import { Public } from "@mui/icons-material";
export default function DicomViewer({axialPath,coronalPath,sagittalPath,selectedFile,Id}) {
  const vti_file =selectedFile.slice(0, -4).concat(".vti") 
  const [slider_1_value, setValue_1] = useState(0);
  const [slider_2_value, setValue_2] = useState(0);
  const [slider_3_value, setValue_3] = useState(0);
  const [isRuler, setIsRuler] = useState(false);
  const [isZoom, setIsZoom] = useState(false);
  const [isRec, setIsRec] = useState(false);
  const [isElip, setIsElip] = useState(false);
  const [isPan, setIsPan] = useState(false);
  const [isAngle,setIsAngle] = useState(false);
  const [isFreeHand,setIsFreeHand] = useState(false);
  const [isRotate,setIsRotate] = useState(false);
  const [loadTool, setLoadTool] = useState(false);
  const [loadTool_2, setLoadTool_2] = useState(false);
  const [loadTool_3, setLoadTool_3] = useState(false);
  const [vtk, setVtk] = useState(null);
  const [response, setresponse] = useState(null);
  function setUpPath(path){
    const scheme = 'wadouri';
    return `${scheme}:${path}`
  }

  const imageIds=axialPath.map(path => setUpPath(path))
  const imageIds2=coronalPath.map(path => setUpPath(path))
  const imageIds3=sagittalPath.map(path => setUpPath(path))
  const [full_ids, setImageIds] = useState(imageIds);
  const [full_ids2, setImageIds2] = useState(imageIds2);
  const [full_ids3, setImageIds3] = useState(imageIds3);
 
   const canvasRef = useRef(null);
   const canvasRef_2 = useRef(null);
   const canvasRef_3 = useRef(null);
   
   const navigate = useNavigate();

   const returnHistory = (e) => {
    navigate(`/history`,{ replace: true })

   };
   const clearMeasure = (e) => {
    var tools =[]
    var elements =[canvasRef.current,canvasRef_2.current,canvasRef_3.current]
    for (let j = 0; j < elements.length; j++) {
        tools.push(cornerstoneTools.getToolState(elements[j], "Length"));
        tools.push(cornerstoneTools.getToolState(elements[j], 'RectangleRoi'));
        tools.push(cornerstoneTools.getToolState(elements[j], 'Zoom'));
        tools.push(cornerstoneTools.getToolState(elements[j], 'EllipticalRoi'));
        tools.push(cornerstoneTools.getToolState(elements[j], 'Pan'));
        tools.push(cornerstoneTools.getToolState(elements[j], 'Angle'));
        tools.push(cornerstoneTools.getToolState(elements[j], 'FreehandRoi'));
        tools.push(cornerstoneTools.getToolState(elements[j], 'Rotate'));
        for (let i = 0; i < tools.length; i++) {

          if (tools[i] ==undefined){
          }else{
            tools[i].data=[]
          }
          
        }
        tools=[]
        cornerstone.updateImage(elements[j]);
      }
  
  };


  if(full_ids.length>0){
  
  useEffect(() => {
    //initialize cornerstone
    cornerstoneTools.external.cornerstone = cornerstone;
    cornerstoneTools.external.cornerstoneMath = cornerstoneMath;
    cornerstoneTools.external.Hammer = Hammer;
    
    //initialize dicom image loader/parser
    cornerstoneWADOImageLoader.external.cornerstone = cornerstone;
    cornerstoneWADOImageLoader.external.dicomParser = dicomParser;
    
    const element = canvasRef.current;
  
    //intial image loading
    const slider_1 = document.getElementById("slider_1");
    cornerstone.loadAndCacheImage(full_ids[100]).then((image) => {
      cornerstone.displayImage(element, image);
      if (full_ids.length > 0) {
        // window.addEventListener("mouseup", swtichOffCross);
        console.log("mouseup added");

        // element.addEventListener("mousemove", handleMouseMoveEvent);
        console.log("mousemove added");

        //load cornerstone tools after intial image loading, else they will not mount properly
        setLoadTool(true);
      }
    });
   
    return () => {
      if (full_ids.length > 0) {
        // element.removeEventListener("mousemove", handleMouseMoveEvent);
        // window.removeEventListener("mouseup", swtichOffCross);
        console.log("mousemove removed");
        console.log("mouseup removed");
      }
    };
  }, [full_ids]);


  useEffect(() => {
    //initialize cornerstone
    cornerstoneTools.external.cornerstone = cornerstone;
    cornerstoneTools.external.cornerstoneMath = cornerstoneMath;
    cornerstoneTools.external.Hammer = Hammer;
    
    //initialize dicom image loader/parser
    cornerstoneWADOImageLoader.external.cornerstone = cornerstone;
    cornerstoneWADOImageLoader.external.dicomParser = dicomParser;
    
    const element = canvasRef_2.current;
  
    //intial image loading
    const slider_2 = document.getElementById("slider_2");
    cornerstone.loadAndCacheImage(full_ids2[100]).then((image) => {
      cornerstone.displayImage(element, image);

      if (full_ids2.length > 0) {
        console.log("mouseup added");

        console.log("mousemove added");

        //load cornerstone tools after intial image loading, else they will not mount properly
        setLoadTool_2(true);
      }
    });
   
    return () => {
      if (full_ids2.length > 0) {
     
        console.log("mousemove removed");
        console.log("mouseup removed");
      }
    };
  }, [full_ids2]);
  
  
  
  useEffect(() => {
    //initialize cornerstone
    cornerstoneTools.external.cornerstone = cornerstone;
    cornerstoneTools.external.cornerstoneMath = cornerstoneMath;
    cornerstoneTools.external.Hammer = Hammer;
    
    //initialize dicom image loader/parser
    cornerstoneWADOImageLoader.external.cornerstone = cornerstone;
    cornerstoneWADOImageLoader.external.dicomParser = dicomParser;
    
    const element = canvasRef_3.current;
  
    //intial image loading
    const slider_3= document.getElementById("slider_3");
    
    cornerstone.loadAndCacheImage(full_ids3[100]).then((image) => {
      cornerstone.displayImage(element, image);

      if (full_ids3.length > 0) {
        console.log("mouseup added");

        console.log("mousemove added");

        //load cornerstone tools after intial image loading, else they will not mount properly
        setLoadTool_3(true);
      }
    });
   
    return () => {
      if (full_ids3.length > 0) {

        console.log("mousemove removed");
        console.log("mouseup removed");
      }
    };
  }, [full_ids3]);

  
  
  useEffect(() => {
    const element = canvasRef.current;
    cornerstone.enable(element);
    cornerstoneTools.init();    
    //1
        cornerstoneTools.addTool(RectangleRoiTool)
    //2
        cornerstoneTools.addToolForElement(element, LengthTool, {
          configuration: {
            drawHandlesOnHover: true,
            deleteIfHandleOutsideImage: true,
            preventContextMenu: true,
          },
        });
    //3
        cornerstoneTools.addTool(ZoomTool, {
          // Optional configuration
          configuration: {
            invert: false,
            preventZoomOutsideImage: false,
            minScale: .1,
            maxScale: 20.0,
          }
        });
    //4
    cornerstoneTools.addTool(EllipticalRoiTool)
    //5
    cornerstoneTools.addTool(PanTool)
    //6
    cornerstoneTools.addTool(AngleTool)
    //7
    cornerstoneTools.addTool(FreehandRoiTool)
    //8
    cornerstoneTools.addTool(RotateTool)

    cornerstoneTools.toolColors.setActiveColor("rgb(0, 255, 0)");
    cornerstoneTools.toolColors.setToolColor("rgb(255, 255, 0)");

    const WwwcTool = cornerstoneTools.WwwcTool;
    cornerstoneTools.addTool(WwwcTool);
    cornerstoneTools.setToolActive("Wwwc", { mouseButtonMask: 4 });

    const stack = {
      currentImageIdIndex: 0,
      imageIds: full_ids,
    };

    const removeMeasurements = (e) => {
      // Get the tool state for the "length" tool
      const toolState = cornerstoneTools.getToolState(element, "Length");

      if (toolState && toolState.data) {
        // Get the currently selected measurement
        toolState.data.forEach((v, i) => {
          if (v.active === true && e.which === 3) {
            // console.log(i);
            toolState.data.splice(i, 1);
            cornerstone.updateImage(element);
          }
        });
      }
    };

    if (loadTool) {
      cornerstoneTools.addStackStateManager(element, ["stack", "Wwc"]);
      cornerstoneTools.addToolState(element, "stack", stack);

      //remove length measurement
      element.addEventListener("mousedown", removeMeasurements);
      console.log("mousedown added");
    }

    return () => {
      if (loadTool) {
        element.removeEventListener("mousedown", removeMeasurements);
        console.log("mousedown removed");
      }
    };
  }, [loadTool]);


  useEffect(() => {
    const element = canvasRef_2.current;
    cornerstone.enable(element);
    cornerstoneTools.init();

    //1
    cornerstoneTools.addTool(RectangleRoiTool)
    //2
        cornerstoneTools.addToolForElement(element, LengthTool, {
          configuration: {
            drawHandlesOnHover: true,
            deleteIfHandleOutsideImage: true,
            preventContextMenu: true,
          },
        });
    //3
        cornerstoneTools.addTool(ZoomTool, {
          // Optional configuration
          configuration: {
            invert: false,
            preventZoomOutsideImage: false,
            minScale: .1,
            maxScale: 20.0,
          }
        });
    //4
    cornerstoneTools.addTool(EllipticalRoiTool)
    //5
    cornerstoneTools.addTool(PanTool)
    //6
    cornerstoneTools.addTool(AngleTool)
    //7
    cornerstoneTools.addTool(FreehandRoiTool)
    //8
    cornerstoneTools.addTool(RotateTool)

    cornerstoneTools.toolColors.setActiveColor("rgb(0, 255, 0)");
    cornerstoneTools.toolColors.setToolColor("rgb(255, 255, 0)");

    const WwwcTool = cornerstoneTools.WwwcTool;
    cornerstoneTools.addTool(WwwcTool);
    cornerstoneTools.setToolActive("Wwwc", { mouseButtonMask: 4 });

    const stack = {
      currentImageIdIndex: 0,
      imageIds: full_ids2,
    };

    const removeMeasurements = (e) => {
      // Get the tool state for the "length" tool
      const toolState = cornerstoneTools.getToolState(element, "Length");

      if (toolState && toolState.data) {
        // Get the currently selected measurement
        toolState.data.forEach((v, i) => {
          if (v.active === true && e.which === 3) {
            // console.log(i);
            toolState.data.splice(i, 1);
            cornerstone.updateImage(element);
          }
        });
      }
    };

    if (loadTool_2) {
      cornerstoneTools.addStackStateManager(element, ["stack", "Wwc"]);
      cornerstoneTools.addToolState(element, "stack", stack);

        //remove length measurement
      element.addEventListener("mousedown", removeMeasurements);
      console.log("mousedown added");
    }

    return () => {
      if (loadTool_2) {
        element.removeEventListener("mousedown", removeMeasurements);
        console.log("mousedown removed");
      }
    };
  }, [loadTool_2]);

  useEffect(() => {
    const element = canvasRef_3.current;
    cornerstone.enable(element);
    cornerstoneTools.init();

    //1
    cornerstoneTools.addTool(RectangleRoiTool)
    //2
        cornerstoneTools.addToolForElement(element, LengthTool, {
          configuration: {
            drawHandlesOnHover: true,
            deleteIfHandleOutsideImage: true,
            preventContextMenu: true,
          },
        });
    //3
        cornerstoneTools.addTool(ZoomTool, {
          // Optional configuration
          configuration: {
            invert: false,
            preventZoomOutsideImage: false,
            minScale: .1,
            maxScale: 20.0,
          }
        });
    //4
    cornerstoneTools.addTool(EllipticalRoiTool)
    //5
    cornerstoneTools.addTool(PanTool)
    //6
    cornerstoneTools.addTool(AngleTool)
    //7
    cornerstoneTools.addTool(FreehandRoiTool)
    //8
    cornerstoneTools.addTool(RotateTool)

    cornerstoneTools.toolColors.setActiveColor("rgb(0, 255, 0)");
    cornerstoneTools.toolColors.setToolColor("rgb(255, 255, 0)");

    const WwwcTool = cornerstoneTools.WwwcTool;
    cornerstoneTools.addTool(WwwcTool);
    cornerstoneTools.setToolActive("Wwwc", { mouseButtonMask: 4 });

    const stack = {
      currentImageIdIndex: 0,
      imageIds: full_ids3,
    };

    const removeMeasurements = (e) => {
      // Get the tool state for the "length" tool
      const toolState = cornerstoneTools.getToolState(element, "Length");

      if (toolState && toolState.data) {
        // Get the currently selected measurement
        toolState.data.forEach((v, i) => {
          if (v.active === true && e.which === 3) {
            // console.log(i);
            toolState.data.splice(i, 1);
            cornerstone.updateImage(element);
          }
        });
      }
    };

    if (loadTool_3) {
      cornerstoneTools.addStackStateManager(element, ["stack", "Wwc"]);
      cornerstoneTools.addToolState(element, "stack", stack);


      //remove length measurement
      element.addEventListener("mousedown", removeMeasurements);
      console.log("mousedown added");
    }

    return () => {
      if (loadTool_3) {
        element.removeEventListener("mousedown", removeMeasurements);
        console.log("mousedown removed");
      }
    };
  }, [loadTool_3]);




  const handleScroll = (e) => {
    
    const slider_1 = document.getElementById("slider_1")
    if (e.deltaY < 0 && slider_1_value < full_ids.length - 1) {
      const new_value = slider_1_value + 1
      setValue_1(new_value);
      slider_1.value=new_value

    } else if (e.deltaY > 0 && slider_1_value > 0) {
      const new_value = slider_1_value -1
      setValue_1(new_value);
      slider_1.value=new_value
     
    }
  };

  const handleScroll_2 = (e) => {
    const slider_2 = document.getElementById("slider_2")
    if (e.deltaY < 0 && slider_2_value < full_ids2.length - 1) {
      const new_value = slider_2_value + 1
      setValue_2(new_value);
      slider_2.value=new_value
    } else if (e.deltaY > 0 && slider_2_value > 0) {
      const new_value = slider_2_value -1
      setValue_2(new_value);
      slider_2.value=new_value
    }
  };

  const handleScroll_3 = (e) => {
    const slider_3 = document.getElementById("slider_3")
    if (e.deltaY < 0 && slider_3_value < full_ids3.length - 1) {
      
      const new_value = slider_3_value + 1
      setValue_3(new_value);
      slider_3.value=new_value
    } else if (e.deltaY > 0 && slider_3_value > 0) {

      const new_value = slider_3_value -1
      setValue_3(new_value);
      slider_3.value=new_value
    }
  };

 

  useEffect(() => {
    const element = canvasRef.current;

    element.addEventListener("wheel", handleScroll);
    cornerstone.loadAndCacheImage(full_ids[slider_1_value]).then((image) => {
      cornerstone.displayImage(element, image);
    });

    return () => {
      element.removeEventListener("wheel", handleScroll);
    };
  }, [slider_1_value]);

  useEffect(() => {
    const element = canvasRef_2.current;

    element.addEventListener("wheel", handleScroll_2);
    cornerstone.loadAndCacheImage(full_ids2[slider_2_value]).then((image) => {
      cornerstone.displayImage(element, image);
    });

    return () => {
      element.removeEventListener("wheel", handleScroll_2);
    };
  }, [slider_2_value]);

  useEffect(() => {
    const element = canvasRef_3.current;

    element.addEventListener("wheel", handleScroll_3);
    cornerstone.loadAndCacheImage(full_ids3[slider_3_value]).then((image) => {
      cornerstone.displayImage(element, image);
    });

    return () => {
      element.removeEventListener("wheel", handleScroll_3);
    };
  }, [slider_3_value]);
 
  useEffect(() => {
    if (isRuler) {
      cornerstoneTools.setToolActive("Length", {
        mouseButtonMask: 1,
      });
    } else {
      cornerstoneTools.setToolEnabled("Length");
    }
  }, [isRuler]);
  useEffect(() => {
    if (isZoom) {
      cornerstoneTools.setToolActive('Zoom', { mouseButtonMask: 1 })
    } else {
      cornerstoneTools.setToolEnabled("Zoom");
    }
  }, [isZoom]);
  useEffect(() => {
    if (isRec) {
      cornerstoneTools.setToolActive('RectangleRoi', { mouseButtonMask: 1 })

    } else {
      cornerstoneTools.setToolEnabled("RectangleRoi");
    }
  }, [isRec]);
  useEffect(() => {
    if (isElip) {
      cornerstoneTools.setToolActive('EllipticalRoi', { mouseButtonMask: 1 })

    } else {
      cornerstoneTools.setToolEnabled("EllipticalRoi");
    }
  }, [isElip]);
  useEffect(() => {
    if (isPan) {
      cornerstoneTools.setToolActive('Pan', { mouseButtonMask: 1 })

    } else {
      cornerstoneTools.setToolEnabled("Pan");
    }
  }, [isPan]);
  useEffect(() => {
    if (isAngle) {
      cornerstoneTools.setToolActive('Angle', { mouseButtonMask: 1 })
    } else {
      cornerstoneTools.setToolEnabled("Angle");
    }
  }, [isAngle]);
  useEffect(() => {
    if (isFreeHand) {
      cornerstoneTools.setToolActive('FreehandRoi', { mouseButtonMask: 1 })
    } else {
      cornerstoneTools.setToolEnabled("FreehandRoi");
    }
  }, [isFreeHand]);
  useEffect(() => {
    if (isRotate) {
      cornerstoneTools.setToolActive('Rotate', { mouseButtonMask: 1 })
    } else {
      cornerstoneTools.setToolEnabled("Rotate");
    }
  }, [isRotate]);




  useEffect(()=>{
    (async function(){
      try {
        let response=''
       response= await axios.get(serverConfig.server_url+"images/predict/"+Id)
       console.log("TTTTTTTTTTTTTTTT")
        setresponse(response)
        return (response);
      
      } catch (error) {
        console.log(error)
      }

      })()

  },[vtk])

  useEffect(()=>{
    console.log("BBBBBBBBBB")

    const element_4 = document.getElementById("canvasRef_4");
    initLocalFileLoader(element_4,vti_file)
    console.log("test")
  },[response])

  // const getPDF = () => 
  // {

  //   const report = new JsPDF('portrait','pt','a4');
  //   var a = report.html(document.getElementById('test1'))
  //   a.save('report.pdf');
  //   var a = report.html(document.getElementById('test2'))
  //   a.save('report2.pdf');
  //   const PDFMerger = require('pdf-merger-js');

    // var merger = new PDFMerger();
    
    // (async () => {
    //   await merger.add('report1.pdf');  //merge all pages. parameter is the path to file and filename.
    //   await merger.add('report2.pdf');  //merge all pages. parameter is the path to file and filename.
      
    //   console.log("oooooooooo")
    //   await merger.save('merged.pdf'); //save under given name and reset the internal document
      
    //   // Export the merged PDF as a nodejs Buffer
    //   // const mergedPdfBuffer = await merger.saveAsBuffer();
    //   // fs.writeSync('merged.pdf', mergedPdfBuffer);
    // })();
 
}
  return (
    <>
    <div className="piechart">
      <Pie_chart Id={Id} />
    </div>
   
      <div className="grid-container">
      <div>

          <div
            ref={canvasRef}
            className="viewer"
            onContextMenu={(e) => {
              e.preventDefault();
              return false;
            }}
            
          > 
          </div>

          <div
          className="slider">
          {/* <Box width={500}> */}
          <Slider defaultValue={0} aria-label="Default" valueLabelDisplay="auto" onChange={(e) => setValue_1(e.target.value*1)}  max={full_ids.length-1} id="slider_1" />
          {/* <input type="range" min="0" max={full_ids.length-1} defaultValue="0" onChange={(e) => setValue_1(e.target.value*1)} className="slider_1" id="slider_1"/> */}
          {/* </Box> */}

          </div>
      </div>

      <div >
          <div
            ref={canvasRef_2}
            className="viewer_2"
            onContextMenu={(e) => {
              e.preventDefault();
              return false;
            }}
            
          > 
          </div>

          <div
          className="slider">
          {/* <Box width={500}> */}
          {/* <Slider defaultValue={0} aria-label="Default" valueLabelDisplay="auto" onChange={(_, v) => setValue(v)} max={110} /> */}


          <Slider defaultValue={0} aria-label="Default" valueLabelDisplay="auto" onChange={(e) => setValue_2(e.target.value*1)} max={full_ids2.length-1}  id="slider_2"/>
          {/* <input type="range" min="0" max={full_ids2.length-1} defaultValue="0" onChange={(e) => setValue_2(e.target.value*1)} className="slider_1" id="slider_2"/>  */}
          {/* </Box> */}

          </div>
      
      </div>
      <div  >
          <div
            ref={canvasRef_3}
            className="viewer_3"
            onContextMenu={(e) => {
              e.preventDefault();
              return false;
            }}
            
          > 
          </div>

          <div
          className="slider_2">
          {/* <Box width={500}> */}
          <Slider defaultValue={0} aria-label="Default" valueLabelDisplay="auto" onChange={(e) => setValue_3(e.target.value*1)} max={full_ids3.length-1} id="slider_3" />
          {/* <input type="range" min="0" max={full_ids3.length-1} defaultValue="0" onChange={(e) => setValue_3(e.target.value*1)} className="slider_1"  id="slider_3"/> */}
          {/* </Box> */}

          </div>
      </div>
      <div >
          <div
                id="canvasRef_4"
                className="viewer_4"
                onContextMenu={(e) => {
                  e.preventDefault();
                  return false;
                }}
              > 
              </div>

              
      </div>
      </div>

      <div className='toolbar'>
      {/* <Button variant="contained"  className='toolbarbutton' style={{ color: "#3d5997" }} startIcon={<OpenInBrowserIcon className="icon"/>}>
       <span className="button-text">Browse</span>
      </Button> */}
      {/* <button variant="contained"  className='toolbarbutton' style={{ color: "white" }}> <OpenInBrowserIcon className="icon" />
       <span className="button-text">Browse</span>
    </button> */}
      <button variant="contained"  onClick={clearMeasure} className='toolbarbutton' style={{ color: "white" }}> <ClearIcon className="icon"/>
      <span className="button-text">Clear</span>
      </button>
      <button variant="contained"  onClick={setIsRuler} className='toolbarbutton' style={{ color: "white" }}> <StraightenIcon className="icon"/>
      <span className="button-text">Ruler</span> 
      </button>
      <button variant="contained"  onClick={setIsZoom} className='toolbarbutton' style={{ color: "white" }}> <ZoomInIcon className="icon"/>
      <span className="button-text">Zoom</span> 
      </button>
      <button variant="contained"  onClick={setIsRec} className='toolbarbutton' style={{ color: "white" }}> <Crop169Icon  className="icon"/>
      <span className="button-text">Rectangle</span>
      </button>
      <button variant="contained"  onClick={setIsElip} className='toolbarbutton' style={{ color: "white" }}> <PanoramaFishEyeIcon  className="icon"/>
      <span className="button-text">Elipse</span>
      </button>
      <button variant="contained"  onClick={setIsPan} className='toolbarbutton' style={{ color: "white" }} > <PanToolIcon  className="icon"/>
      <span className="button-text">Pan</span>
      </button>
      <button variant="contained"  onClick={setIsAngle} className='toolbarbutton' style={{ color: "white" }}> <TextRotationAngleupIcon  className="icon"/>
      <span className="button-text">Angle</span>
      </button>
      <button variant="contained"  onClick={setIsFreeHand} className='toolbarbutton' style={{ color: "white" }}> <CheckBoxOutlineBlankIcon  className="icon"/>
      <span className="button-text">ROI</span>
      </button>
      <button variant="contained"  onClick={setIsRotate} className='toolbarbutton' style={{ color: "white" }}> <LoopIcon  className="icon"/>
      <span className="button-text">Rotate</span>
      </button>
      {/* <button variant="contained"  className='toolbarbutton' style={{ color: "white" }}><GetAppIcon  className="icon"/>
      <span className="button-text">Export</span>
      </button> */}
      <button variant="contained"  onClick={returnHistory} className='toolbarbutton' style={{ color: "white" }}><HistoryIcon  className="icon"/>
      <span className="button-text">History</span>
      </button>
      </div>

    </>
  );
}
