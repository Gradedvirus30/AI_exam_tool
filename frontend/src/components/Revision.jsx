import axios from "axios";
import { useState } from "react";

function Revision(){

const [topic,setTopic]=useState("");
const [revision,setRevision]=useState("");

const generateRevision=async()=>{

const response=await axios.post(

"https://aiexamtool-production.up.railway.app/revision",

{
topic
}

);

setRevision(
response.data.revision
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

🧠 Generate

</button>

<p>{revision}</p>

</div>

);

}

export default Revision;