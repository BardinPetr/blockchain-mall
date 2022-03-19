import { BrowserRouter, Routes, Route } from "react-router-dom";

import MetamaskAuth from "./views/MetamaskAuth";
import Rooms from "./views/Rooms";
import CreateRoom from "./views/CreateRoom";
import Room from "./views/Room";
import RoomEdit from "./views/RoomEdit";
import Cashiers from "./views/Cashiers";
import Ticket from "./views/Ticket";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MetamaskAuth />} />
        <Route path="/rooms/" element={<Rooms />} />
        <Route path="/rooms/create" element={<CreateRoom />} />
        <Route path="/room/:id" element={<Room />} />
        <Route path="/room/:id/cashiers" element={<Cashiers />} />
        <Route path="/room/:id/edit" element={<RoomEdit />} />
        <Route path="/ticket/:id" element={<Ticket />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
