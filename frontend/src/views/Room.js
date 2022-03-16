import { useParams } from "react-router-dom";

function Room() {
  const { id } = useParams();
  return (
    <>
      <h4>Room id: {id}</h4>
    </>
  )
}

export default Room;
