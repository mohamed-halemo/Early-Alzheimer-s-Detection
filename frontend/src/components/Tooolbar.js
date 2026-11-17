import React, { useState } from 'react';
import Button from "@material-ui/core/Button";
// import Toolbar from "@material-ui/core/Toolbar";
import OpenInBrowserIcon from '@mui/icons-material/OpenInBrowser';
import axios from "axios";
import serverConfig from '../server_config.json';
import DicomViewer from './DicomViewer';

function Tooolbar() {

  const [axialPath, setAxialPath] = useState([]);
  const [coronalPath, setCoronalPath] = useState([]);
  const [sagittalPath, setSagittalPath] = useState([]);
  const [selectedFile, setSelectedFile] = useState([]);


  const handleselectedFile = event => {
    // console.log(event.target.files[0],'iiiiiiii');
    setSelectedFile(event.target.files[0]);
    var data = new FormData();
      data.append("media_file",event.target.files[0]);
      // console.log(data);
      (async function(){
      try {
        let response = '';
  
        response = await axios.post(serverConfig.server_url+'images/upload', data)
        
        console.log(response.data)
        setAxialPath(response.data["axial"])
        setCoronalPath(response.data["coronal"])
        setSagittalPath(response.data["sagittal"])

        
        return (response);
      } catch (error) {
        console.log(error)
      }
    })()
  }


  return (
      
    
      <div className="browse-button-container">
      <div className='toolbar'>
      <label className='toolbarbutton' >
        <OpenInBrowserIcon className="icon" />
        <input type="file"  id="" onChange={handleselectedFile}/>
        <span className="button-text">Browse</span>
        </label> 
    <input id="actual-upload" type="file" />
  
    </div>
          {   selectedFile != null && axialPath.length>0 && coronalPath.length>0 && sagittalPath.length>0 &&(<DicomViewer axialPath={axialPath}  coronalPath={coronalPath} sagittalPath={sagittalPath} selectedFile={selectedFile}/>)}
          
    </div>

  );
}

export default Tooolbar;