// import React, { useState } from 'react';
// import DicomViewer from './DicomViewer';
// import axios from "axios";
// import serverConfig from '../server_config.json';

// const BrowseButton = () => {
//   const [folderName, setFolderName] = useState('');
//   const [filePaths, setFilePaths] = useState([]);
//   const [loaded, setloaded] = useState(0);
//   const [selectedFile, setselectedFile] = useState(null);


//   const handleselectedFile = event => {
//     setselectedFile(event.target.files[0]);
//     setloaded(0)
//   }

//   const handleUpload = () => {
//     var data = new FormData();
//     // console.log(data);
//     console.log(selectedFile);
//     data.append("media_file",selectedFile);
//     // console.log(data);
//     (async function(){
//     try {
//       let response = '';

//       response = await axios.post(serverConfig.server_url+'images/upload', data, {
//             onUploadProgress: ProgressEvent => {
//                 setloaded(ProgressEvent.loaded / ProgressEvent.total*100)
//             },
//           })
  
//       console.log(response)
//       return (response);
//     } catch (error) {
//       if (error.response) {
//         /*
//             * The request was made and the server responded with a
//             * status code that falls out of the range of 2xx
//             */
//           console.log("ooooooooooooooo1")
//           // console.log(error.response.data);
//           // console.log(error.response.status);
//           // console.log(error.response.headers);
//         return (error.response);
//       } if (error.request) {
//         /*
//             * The request was made but no response was received, `error.request`
//             * is an instance of XMLHttpRequest in the browser and an instance
//             * of http.ClientRequest in Node.js
//             */
//         console.log("ooooooooooooooo2");
//         console.log(error.request);
//       } else {
//         // Something happened in setting up the request and triggered an Error
//         console.log("ooooooooooooooo3");
        
//         console.log('Error', error.message);
//       }
//       console.log("ooooooooooooooo4");
//       console.log(error);
//       return (response);
//     }
//   })()
// }

//   const handleFolderSelection = (event) => {
//     const files = event.target.files;
//     // console.log(files)
//     if (files.length > 0) {
//       const folder = files[0].webkitRelativePath.split('/')[0];
//       setFolderName(folder);
//       const paths = [];
//       for (let i = 0; i < files.length; i++) {
//         const path = files[i].webkitRelativePath;
//         paths.push(path);
//       }
//       setFilePaths(paths);
//     }
//   }

//   return (
//     <div>
      
//     <div className="browse-button-container">
      
//     <DicomViewer folderName={folderName}  filePaths={filePaths}  />
         
        
//     </div>

    

//     </div>
//   );
// }

// export default BrowseButton;
