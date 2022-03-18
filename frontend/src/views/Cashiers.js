import { useState, useEffect } from "react";
import { gqlPost } from "../tools/tools";
import { useParams } from "react-router-dom";
import { GET_CASHIERS } from "../gql/queries";
import { ADD_CASHIER } from "../gql/mutations";

import Input from "./Input";
import Button from "./Button";

function Cashiers() {
  const { id } = useParams();
  const [addresses, setAddresses] = useState([]);
  const [newAddress, setNewAddress] = useState("");
  useEffect(async () => {
    const d = await gqlPost(GET_CASHIERS, { id });
    const data = d.data;
    console.log(d);
    setAddresses(data);
  }, []);

  const sumbitCashier = async () => {
    const d = await gqlPost(ADD_CASHIER, { id, address: newAddress });
    console.log(d);
  }

  return (
    <>
      <p>cashiers</p>
      {addresses && (
        <ul className="cashiers">
          {addresses.map((address) => (
            <li className="cashier__address">{address}</li>
          ))}
        </ul>
      )}
      <form className="add-cashier" onSubmit={sumbitCashier}>
        <Input
          type="text"
          k="add-cashier__address"
          cb={(e) => setNewAddress(e.target.value)}
          v={newAddress}
          required
        />
        <Button type="submit" k="add_cashier__submit" />
      </form>
    </>
  );
}

export default Cashiers;
