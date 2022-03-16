import { BrowserRouter, Routes, Route } from "react-router-dom";

import MetamaskAuth from "./views/MetamaskAuth";
import Rooms from "./views/Rooms";
import CreateRoom from "./views/CreateRoom";
import Room from "./views/Room";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MetamaskAuth />} />
        <Route path="/rooms/" element={<Rooms />} />
        <Route path="/rooms/create" element={<CreateRoom />} />
        <Route path="/room/:id" element={<Room />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
