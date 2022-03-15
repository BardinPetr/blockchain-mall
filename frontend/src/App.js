import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import MetamaskAuth from "./views/MetamaskAuth";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MetamaskAuth/>} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
