
import React from 'react';
import Logo from './Logo';
import Tooolbar from './Tooolbar';
import { useParams} from 'react-router-dom';
import { useState,useEffect } from 'react';
import axios from "axios";
import serverConfig from '../server_config.json';
import DicomViewer from './DicomViewer';




function Visualization () {
  let {Id} = useParams()
  const [axialPath, setAxialPath] = useState([]);
  const [coronalPath, setCoronalPath] = useState([]);
  const [sagittalPath, setSagittalPath] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [vtk, setVtk] = useState(null);

  useEffect(() => {

    (async function(){
      try {
        let response = '';
  
        response = await axios.get(serverConfig.server_url+"images/study/"+Id)
        
        setSelectedFile(response.data["selected_file"])
        setAxialPath(response.data["axial"])
        setCoronalPath(response.data["coronal"])
        setSagittalPath(response.data["sagittal"])
        
        return (response);
      } catch (error) {
        console.log(error)
      }
    })()
  },[vtk])

  

 return (
    <div >
      <Logo />
      {   selectedFile != null && axialPath.length>0 && coronalPath.length>0 && sagittalPath.length>0 &&(<DicomViewer axialPath={axialPath}  coronalPath={coronalPath} sagittalPath={sagittalPath} selectedFile={selectedFile} Id={Id}/>)}
      </div>
       ); 

      
}

export default Visualization;