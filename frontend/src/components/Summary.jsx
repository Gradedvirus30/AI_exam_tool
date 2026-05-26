import axios from "axios";
import { useState } from "react";

function Summary(){

const [topic,setTopic]=useState("");

const [summary,setSummary]=useState("");


const generateSummary=async()=>{

try{

const response=
await axios.post(
"https://aiexamtool-production.up.railway.app/summary",
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
setTopic(
e.target.value
)
}

/>


<button
onClick={askQuestion}
disabled={loading}
>

{loading
?
"⏳ Generating..."
:
"❓ Ask"}

</button>


<div className="response-box">

<pre>

{summary}

</pre>

</div>

</div>

);

}

export default Summary;