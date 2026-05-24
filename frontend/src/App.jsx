import "./App.css";
import axios from "axios";
import { useState } from "react";

function App() {

  const [file, setFile] = useState(null);

  const [message, setMessage] = useState("");


  const uploadPDF = async () => {

    if (!file) {

      setMessage(
        "Please choose a PDF"
      );

      return;
    }

    const formData =
    new FormData();

    formData.append(
      "file",
      file
    );

    try {

    const response =
    await axios.post(
        "http://127.0.0.1:8000/upload",
        formData
    );

    console.log(
      "Backend response:",
      response.data
    );

    setMessage(
      `Uploaded successfully: ${response.data.filename}`
    );

}
    catch (error) {

    console.log(
      "FULL ERROR:",
      error
    );

    if(error.response){

      console.log(
        error.response.data
      );

    }

    setMessage(
      `Error: ${error.message}`
    );

}

  };


  return (

    <div className="app">

      <div className="sidebar">

        <h2>AI Exam Assistant</h2>

        <button>📄 Upload PDF</button>

        <button>❓ Ask</button>

        <button>📝 Summary</button>

        <button>🧠 Revision</button>

        <button>🎯 Quiz</button>

        <button>🗂 Flashcards</button>

      </div>


      <div className="main">

        <h1>Dashboard</h1>

        <div className="card">

          <h3>Upload Notes</h3>

          <input
            type="file"
            accept=".pdf"
            onChange={(e) => {

              const selectedFile =
              e.target.files[0];

              setFile(
                selectedFile
              );

            }}
          />

          <button
            onClick={uploadPDF}
          >

            Upload

          </button>


          <p className="warning">

            ⚠ Recommended:
            Keep PDFs under 100 pages
            for faster processing and better performance

          </p>


          <p>

            {message}

          </p>

        </div>

      </div>

    </div>

  );

}

export default App;