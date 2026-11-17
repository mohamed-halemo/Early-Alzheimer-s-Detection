import Register from './components/Register';
import Login from './components/Login';
import Visualization from './components/Visualization';
import React, { useEffect, useState } from "react";
import History from './components/History'
import { Routes, Route, BrowserRouter as Router} from 'react-router-dom';
import WarningMessages from './components/WarningMessages';
import TutorialDataService from "./serves/TutorialDataService";
import { async } from 'q';



function App() {
  const [patientData, setpatientData] = useState([]);

  useEffect(() => {
    (async function(){
    await TutorialDataService.getAll()
    .then((response) => {
      // setTutorials(response.data);
      for (let j = 0; j < response.data.length; j++) {
        patientData.push({ study_id: response.data[j].name, patient_id: response.data[j].owner.name , patient_name: 'Anonymous', date:  response.data[j].date_created.split('T')[0] , class:  response.data[j].predicted_class })}
      setpatientData(patientData)
    })
    .catch((e) => {
      console.log(e);
    });})()
  }, [patientData]);

  let response =""
    
  return (
    <main className="App">
    <Router>
      <Routes>
      <Route path="/" element={<Login />}/>
      <Route path="/register" element={<Register />}/>
      <Route path="/:Id" element={<Visualization/>}/>
      
      <Route path="/history" element={<History patientData={patientData} />}/>
      <Route path="/messages" element={<WarningMessages />}/>
   
      </Routes>
      </Router> 
      </main>

 
  );
}

export default App;