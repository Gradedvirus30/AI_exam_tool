import axios from "axios";
import {useState} from "react";

function Upload(){

const [file,setFile]=useState(null);

const [message,setMessage]=useState("");


const uploadPDF=async()=>{

if(!file){

setMessage(
"Please choose a PDF"
);

return;
}

const formData=
new FormData();

formData.append(
"file",
file
);

try{

const response=
await axios.post(
"http://127.0.0.1:8000/upload",
formData
);

setMessage(
`Uploaded successfully:
${response.data.filename}`
);

}

catch{

setMessage(
"Upload failed"
);

}

};


return(

<div className="card">

<h3>Upload Notes</h3>

<input
type="file"
accept=".pdf"

onChange={(e)=>
setFile(
e.target.files[0]
)
}
/>

<button
onClick={uploadPDF}
>

Upload

</button>

<p className="warning">

⚠ Recommended:
Keep PDFs under 100 pages
for faster processing

</p>

<p>

{message}

</p>

</div>

);

}

export default Upload;