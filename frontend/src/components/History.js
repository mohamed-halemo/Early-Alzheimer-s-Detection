import React, { useEffect, useState } from "react";
import VisibilityIcon from '@mui/icons-material/Visibility';
import DeleteIcon from '@mui/icons-material/Delete';
import Logo from './Logo';
import { Navigate, useNavigate } from 'react-router-dom';
import OpenInBrowserIcon from '@mui/icons-material/OpenInBrowser';
import axios from "axios";
import serverConfig from '../server_config.json';
import DicomViewer from './DicomViewer';
import LogoutIcon from '@mui/icons-material/Logout';
import { Logout } from "@mui/icons-material";
const History = ({ patientData }) => {

  const navigate = useNavigate();
  const [searchQueries, setSearchQueries] = useState({
    patientId: '',
    StudyId: '',
    patientName: '',
    date: '',
    class: '',
  });
  const routeChange = (e) => {
    navigate(`/`)

   };


  const [patients, setPatients] = useState(patientData);

  const handleSearch = (event, columnName) => {
    setSearchQueries((prevSearchQueries) => ({
      ...prevSearchQueries,
      [columnName]: event.target.value,
    }));
  };
  const [selectedFile, setSelectedFile] = useState([]);


  const handleselectedFile = event => {
    setSelectedFile(event.target.files[0]);
    var data = new FormData();
      data.append("media_file",event.target.files[0]);
      (async function(){
      try {
        let response = '';
  
        response = await axios.post(serverConfig.server_url+'images/upload', data)
        
        console.log(response.data)

        let id = response.data["id"]
        navigate(`/${id}`,{ replace: true })
        
        return (response);
      } catch (error) {
        console.log(error)
      }
    })()
  }
  const handleDelete = (StudyId) => {
    const updatedPatients = patients.filter((patient) => patient.study_id !== StudyId);
    setPatients(updatedPatients);
  };
  function test(event){
    let id = event.target.innerText
    navigate(`/${id}`,{ replace: true })
  }


  const filteredData = patients.filter(
    (patient) =>
      (patient.study_id || '')
        .toString()
        .toLowerCase()
        .includes(searchQueries.StudyId.toLowerCase()) &&
      patient.patient_name.toLowerCase().includes(searchQueries.patientName.toLowerCase()) &&
      patient.patient_id.toLowerCase().includes(searchQueries.patientId.toLowerCase()) &&
      patient.date.toLowerCase().includes(searchQueries.date.toLowerCase()) &&
      patient.class.toLowerCase().includes(searchQueries.class.toLowerCase()) 
      // patient.age.toLowerCase().includes(searchQueries.age.toLowerCase())

      );

  return (
    <div className="history-container">
      <Logo />
      {/* <div className="browse-button-container">
      <div className='toolbar'>
      <label className='toolbarbutton' >
        <OpenInBrowserIcon className="icon" />
        <input type="file"  id="" onChange={handleselectedFile}/>
        <span className="button-text">Browse</span>
        </label> 
    <input id="actual-upload" type="file" />
  
    </div>
          
    </div> */}


    <div className="browse-button-container">
    {/* <div className='toolbar'> */}

      {/* <label htmlFor="button" className="browse-button-label">Select DICOM Folder</label> */}
      {/* <OpenInBrowserIcon className="icon_browse" /> */}
      <input type="file" id="button" className="browse-button-input" onChange={handleselectedFile} />
      {selectedFile.length > 0 && (
        <div className="selected-folder">
          {/* <p className="folder-name">File name: {selectedFile}</p> */}
        </div>
      )}
      <div className='bar'>
      {/* <Button variant="contained"  className='toolbarbutton' style={{ color: "#3d5997" }} startIcon={<OpenInBrowserIcon className="icon"/>}>
       <span className="button-text">Browse</span>
      </Button> */}
      {/* <button variant="contained"  className='toolbarbutton' style={{ color: "white" }}> <OpenInBrowserIcon className="icon" />
       <span className="button-text">Browse</span>
    </button> */}
      <button variant="contained" onClick={routeChange} className='toolbarbutton' style={{ color: "white" }}> <Logout className="icon"/>
      <span className="button-text">Logout</span>
      </button>
      </div>
    </div>
    {/* </div> */}
      <div className="history-table-container" data-simplebar>
      <table className="history-table">
        <thead>
          <tr>
            <th></th>
            <th>
            <div className="column-header">
                <span>Study ID</span>
                <input
                  type="text"
                  value={searchQueries.StudyId}
                  onChange={(e) => handleSearch(e, 'StudyId')}
                  placeholder="Search..."
                />
              </div>
            </th>
            <th>
            <div className="column-header">
                <span>Patient ID</span>
                <input
                  type="text"
                  value={searchQueries.patientId}
                  onChange={(e) => handleSearch(e, 'patientId')}
                  placeholder="Search..."
                />
              </div>
            </th>
            <th>
              <div className="column-header">
                <span>Patient Name</span>
                <input
                  type="text"
                  value={searchQueries.patientName}
                  onChange={(e) => handleSearch(e, 'patientName')}
                  placeholder="Search..."
                />
              </div>
            </th>
            <th >
              <div className="column-header">
                <span>Date</span>
                <input
                  type="text"
                  value={searchQueries.date}
                  onChange={(e) => handleSearch(e, 'date')}
                  placeholder="Search..."
                />
              </div>
            </th>
            
            <th className="small-column">
              <div className="column-header">
                <span>Class</span>
                <div className="custom-select-wrapper">
                  <select
                    value={searchQueries.class}
                    onChange={(e) => handleSearch(e, 'class')}
                    className="custom-select"
                  >
                    <option value="">All</option>
                    <option value="cn">CN</option>
                    <option value="ad">AD</option>
                    <option value="mci">MCI</option>
                  </select>
                </div>
              </div>
            </th>
            {/* <th className="last-column"></th> */}
          </tr>
        </thead>

        <tbody>
          {filteredData.map((patient) => (
            <tr key={patient.study_id} >
              <td>
                <VisibilityIcon />
              </td>
              <td onClick={test}>{ patient.study_id }</td>
              <td>{patient.patient_id}</td>
              <td>{patient.patient_name}</td>
              <td>{patient.date}</td>
              <td className="small-column">{patient.class}</td>
              {/* <td className="last-column">
                <DeleteIcon onClick={() => handleDelete(patient.id)} />
              </td> */}
            </tr>
          ))}
        </tbody>
      </table>
      </div>
     
    </div>
  );
};

export default History;
