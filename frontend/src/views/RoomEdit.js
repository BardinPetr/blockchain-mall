import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import Input from "./Input";
import Button from "./Button";
import { GET_ROOM_FOR_EDIT } from "../gql/queries";
import { EDIT_ROOM } from "../gql/mutations";
import { gqlPost, isLandlord } from "../tools/tools";

function RoomEdit() {
  const { id } = useParams();
  const [internalName, setInternalName] = useState("");
  const [area, setArea] = useState(0);
  const [location, setLocation] = useState("");

  useEffect(async () => {
    const d = await gqlPost(GET_ROOM_FOR_EDIT, { id });
    const data = d.data.room;
    console.log(data);
    setInternalName(data.internalName);
    setArea(data.area);
    setLocation(data.location);
  }, []);

  const submitEditRoom = (e) => {
    e.preventDefault();
    gqlPost(EDIT_ROOM, { id, internalName, area, location }).then((res) =>
      console.log(res)
    );
  };
  return (
    <>
      {isLandlord && (
        <form className="room-form" onSubmit={submitEditRoom}>
          <Input
            k="room-form__internal-name"
            cb={(e) => setInternalName(Number(e.target.value))}
            type="text"
            value={internalName}
            required
          ></Input>
          <Input
            k="room-form__area"
            cb={(e) => setArea(Number(e.target.value))}
            type="number"
            value={area}
            required
          ></Input>
          <Input
            k="room-form__location"
            cb={(e) => setLocation(e.target.value)}
            type="text"
            value={location}
            required
          ></Input>
          <Button type="submit" k="room-form__submit" />
        </form>
      )}
    </>
  );
}

export default RoomEdit;
