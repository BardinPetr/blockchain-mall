import { useQuery } from "@apollo/client";
import { useState } from "react";

import Field from "./Field";

import { AUTHENTICATION, GET_ALL_ROOMS, STATUSES } from "../gql/queries";

function Rooms() {
  const [address, setAddress] = useState(undefined);
  const [isLandlord, setIsLandlord] = useState(undefined);
  const [rooms, setRooms] = useState([]);
  const { error: isAuthError } = useQuery(AUTHENTICATION, {
    fetchPolicy: "no-cache",
    onCompleted: ({ data }) => {
      setAddress(data.address);
      setIsLandlord(data.landlord);
    },
  });
  useEffect(() => {
    useQuery(isLandlord ? GET_ALL_ROOMS : GET_TENANT_ROOMS, {
      fetchPolicy: "no-cache",
      variables: {
        address: isLandlord ? undefined : address,
      },
      onCompleted: ({ data }) => {
        setRooms(data);
        console.log(data);
      },
    });
  }, [isLandlord]);
  return (
    <>
      {isAuthError && <p>Auth error!</p>}
      {isError && <p>Error!</p>}
      {isLandlord && (
        <a className="rooms__create" href="/rooms/create/">
          rooms__create
        </a>
      )}
      {rooms.map((data) => {
        <div id={`room-${data.id}`} className="room-card">
          <Field k="room-card__name" v={data.publicName} />
          <Field k="room-card__status" v={data.status} />
          <a className="room-card__details" href={`/room/${data.id}`}>
            room-card__details
          </a>
        </div>;
      })}
    </>
  );
}

export default Rooms;
