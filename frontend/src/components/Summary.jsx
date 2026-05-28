import axios from "axios";
import { useState } from "react";
import ReactMarkdown from "react-markdown";

function Summary(){

const [topic,setTopic]=useState("");
const [summary,setSummary]=useState("");

const generateSummary=async()=>{

const response=await axios.post(

"https://aiexamtool-production.up.railway.app/summary",

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

setSummary(
response.data.summary
);

};

const downloadFile=()=>{

const blob=new Blob(

[summary],

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

a.download="summary.txt";

a.click();

window.URL.revokeObjectURL(
url
);

};

return(

<div className="card">

<h3>Summary</h3>

<input
type="text"
placeholder="Enter topic"
value={topic}
onChange={(e)=>setTopic(e.target.value)}
/>

<button onClick={generateSummary}>

Generate

</button>

<div className="response">

<ReactMarkdown>

{summary}

</ReactMarkdown>

</div>

{summary && (

<button onClick={downloadFile}>

⬇ Download

</button>

)}

</div>

);

}

export default Summary;