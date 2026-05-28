import axios from "axios";
import { useState } from "react";
import ReactMarkdown from "react-markdown";

function Revision(){

const [topic,setTopic]=useState("");
const [revision,setRevision]=useState("");

const generateRevision=async()=>{

const response=await axios.post(

"https://aiexamtool-production.up.railway.app/revision",

{
topic
},

{
headers:{

"session-id":
localStorage.getItem(
"session_id"
)

}
}

);

setRevision(
response.data.revision
);

};

const downloadFile=()=>{

const blob=new Blob(

[revision],

{
type:"text/plain"
}

);

const url=
window.URL.createObjectURL(
blob
);

const a=
document.createElement("a");

a.href=url;

a.download="revision.txt";

a.click();

window.URL.revokeObjectURL(
url
);

};

return(

<div className="card">

<h3>Revision</h3>

<input
type="text"
placeholder="Enter topic"
value={topic}
onChange={(e)=>setTopic(e.target.value)}
/>

<button onClick={generateRevision}>

Generate

</button>

<div className="response">

<ReactMarkdown>

{revision}

</ReactMarkdown>

</div>

{revision && (

<button onClick={downloadFile}>

⬇ Download

</button>

)}

</div>

);

}

export default Revision;