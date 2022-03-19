import { useQuery, useLazyQuery } from "@apollo/client";
import { useState, useEffect } from "react";

import Field from "./Field";

import {
  AUTHENTICATION,
  GET_ALL_ROOMS,
  GET_TENANT_ROOMS,
  STATUSES,
} from "../gql/queries";
import { isLandlord, getAddress, gqlPost } from "../tools/tools";

function Rooms() {
  const [address, setAddress] = useState(undefined);
  const [rooms, setRooms] = useState([]);
  useEffect(async () => {
    const d = await gqlPost(isLandlord() ? GET_ALL_ROOMS : GET_TENANT_ROOMS, {
      address: isLandlord() ? getAddress() : undefined,
    });
    console.log(d);
    let data = d.data.rooms;
    console.log(data);
    setRooms(data);
  }, []);

  return (
    <>
      {/*{isAuthError && <p>Auth error!</p>}*/}
      {/* {isError && <p>Error!</p>} */}
      {isLandlord() && (
        <a className="rooms__create" href="/rooms/create">
          rooms__create
        </a>
      )}
      {rooms.map((data) => {
        return (
          <div key={data.id} id={`room-${data.id}`} className="room-card">
            <Field k="room-card__name" v={data.publicName} />
            <Field k="room-card__status" v={STATUSES[data.status % 4]} />
            <a className="room-card__details" href={`/room/${data.id}`}>
              room-card__details
            </a>
          </div>
        );
      })}
    </>
  );
}

export default Rooms;
