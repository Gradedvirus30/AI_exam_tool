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

📝 Generate

</button>

<div className="response">

<ReactMarkdown>

{summary}

</ReactMarkdown>

</div>

</div>

);

}

export default Summary;