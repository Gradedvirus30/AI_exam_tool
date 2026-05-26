import axios from "axios";
import { useState } from "react";

function Revision(){

const [topic,setTopic]=useState("");

const [revision,setRevision]=useState("");


const generateRevision=async()=>{

try{

const response=
await axios.post(
"http://127.0.0.1:8000/revision",
{
topic:topic
}
);

setRevision(
response.data.revision
);

}

catch{

setRevision(
"Failed"
);

}

};



return(

<div className="card">

<h3>Revision Sheet</h3>

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

{revision}

</pre>

</div>

</div>

);

}

export default Revision;