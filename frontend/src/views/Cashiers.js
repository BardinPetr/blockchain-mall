import { useState, useEffect } from "react";
import { gqlPost } from "../tools/tools";
import { useParams } from "react-router-dom";
import { GET_CASHIERS } from "../gql/queries";

function Cashiers() {
  const { id } = useParams();
  const [addresses, setAddresses] = useState([]);
  useEffect(async () => {
    const d = await gqlPost(GET_CASHIERS, { id });
    const data = d.data;
    console.log(d);
    setAddresses(data);
  }, []);

  return (
    <>
      <p>cashiers</p>
      <ul className="cashiers">
        {addresses.map((address) => (
          <li className="cashier__address">{address}</li>
        ))}
      </ul>
    </>
  );
}

export default Cashiers;
