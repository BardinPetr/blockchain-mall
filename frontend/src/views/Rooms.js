import { useQuery } from "@apollo/client";
import { useState } from "react";

import { AUTHENTICATE } from "../gql/queries";

function Rooms() {
  const [address, setAddress] = useState(undefined);
  const [isLandlord, setIsLandlord] = useState(undefined);
  const { error: isError } = useQuery(AUTHENTICATE, {
    fetchPolicy: "no-cache",
    onCompleted: ({ data }) => {
      setAddress(data.address);
      setIsLandlord(data.landlord);
    },
  });
  return (
    <>
      {isLandlord && (
        <a className="rooms__create" href="/rooms/create/">
          rooms__create
        </a>
      )}
      {isError && <p>Error!</p>}
    </>
  );
}

export default Rooms;
