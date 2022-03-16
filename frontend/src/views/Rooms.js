import { useQuery } from "@apollo/client";
import { useState } from "react";

import { AUTHENTICATION } from "../gql/queries";

function Rooms() {
  const [address, setAddress] = useState(undefined);
  const [isLandlord, setIsLandlord] = useState(undefined);
  const { error: isError } = useQuery(AUTHENTICATION, {
    fetchPolicy: "no-cache",
    onCompleted: ({ data }) => {
      setAddress(data.address);
      setIsLandlord(data.landlord);
    },
  });
  return (
    <>
      {isError && <p>Error!</p>}
      {isLandlord && (
        <a className="rooms__create" href="/rooms/create/">
          rooms__create
        </a>
      )}
    </>
  );
}

export default Rooms;
