import axios from "axios";
import { useState } from "react";

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

session_id:
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

<p>{summary}</p>

</div>

);

}

export default Summary;