import "./App.css";

import { useState } from "react";

import Upload from "./components/Upload";
import Ask from "./components/Ask";
import Summary from "./components/Summary";
import Revision from "./components/Revision";
import Quiz from "./components/Quiz";
import Flashcards from "./components/Flashcards";


function App() {

const [activeTab,setActiveTab]=
useState("upload");


return(

<div className="app">

<div className="sidebar">

<h2>AI Exam Assistant</h2>


<button
onClick={()=>
setActiveTab(
"upload"
)
}
>

📄 Upload PDF

</button>


<button
onClick={()=>
setActiveTab(
"ask"
)
}
>

❓ Ask

</button>


<button
onClick={()=>
setActiveTab(
"summary"
)
}
>

📝 Summary

</button>


<button
onClick={()=>
setActiveTab(
"revision"
)
}
>

🧠 Revision

</button>


<button
onClick={()=>
setActiveTab(
"quiz"
)
}
>

🎯 Quiz

</button>


<button
onClick={()=>
setActiveTab(
"flashcards"
)
}
>

🗂 Flashcards

</button>

</div>



<div className="main">

<h1>Dashboard</h1>


{activeTab==="upload"
&& <Upload/>}


{activeTab==="ask"
&& <Ask/>}


{activeTab==="summary"
&& <Summary/>}


{activeTab==="revision"
&& <Revision/>}


{activeTab==="quiz"
&& <Quiz/>}


{activeTab==="flashcards"
&& <Flashcards/>}


</div>

</div>

);

}

export default App;