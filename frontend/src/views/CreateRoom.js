import { useMutation } from "@apollo/client";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { CREATE_ROOM, GET_ACCESS_TOKEN } from "../gql/mutations";

import { gqlPost } from "../tools/tools"

function CreateRoom() {
  const nav = useNavigate();

  const [internalName, setInternalName] = useState("");
  const [area, setArea] = useState(0);
  const [location, setLocation] = useState("");

  // const [createRoomMutation] = useMutation(CREATE_ROOM, {
  //   onCompleted: ({ createRoom }) => {
  //     nav(`/room/${createRoom.id}`);
  //   },
  // });

  const createRoomSubmit = (e) => {
    e.preventDefault();
    // createRoomMutation({
    //   variables: {
    //     room: {
    //       internalName: internalName,
    //       area: area,
    //       location: location,
    //     },
    //   },
    // });
    gqlPost(CREATE_ROOM, {
        room: {
          internalName: internalName,
          area: area,
          location: location,
        },
    }).then((data) => {
      console.log(data);
    });
  };

  return (
    <>
      <form className="room-form" onSubmit={createRoomSubmit}>
        <input
          type="text"
          className="room-form__internal-name"
          placeholder="room-form__internal-name"
          required
          onInput={(e) => setInternalName(e.target.value)}
        />
        <input
          type="number"
          className=".room-form__area"
          placeholder=".room-form__area"
          required
          onInput={(e) => setArea(Number(e.target.value))}
        />
        <input
          type="text"
          className="room-form__location"
          placeholder="room-form__location"
          required
          onInput={(e) => setLocation(e.target.value)}
        />
        <button type="sumbit" className="room-form__submit">
          room-form__submit
        </button>
      </form>
    </>
  );
}

export default CreateRoom;
