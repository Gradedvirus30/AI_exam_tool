import axios from "axios";
import {useState} from "react";

function Summary(){

const [topic,setTopic]=useState("");
const [summary,setSummary]=useState("");

const generateSummary=async()=>{

try{

const response=
await axios.post(
"http://127.0.0.1:8000/summary",
{
topic:topic
}
);

setSummary(
response.data.summary
);

}

catch{

setSummary(
"Failed"
);

}

};

return(

<div className="card">

<h3>Summary</h3>

<input
type="text"
placeholder="Enter topic..."
value={topic}

onChange={(e)=>
setTopic(e.target.value)
}
/>

<button onClick={generateSummary}>
Generate
</button>

<p>{summary}</p>

</div>

);

}

export default Summary;