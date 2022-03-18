import { useQuery } from "@apollo/client";
import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";

import { GET_ROOM, STATUSES } from "../gql/queries";
import { EDIT_PUBLIC_NAME } from "../gql/mutations";
import { gqlPost, isLandlord } from "../tools/tools";

import Button from "./Button";
import Field from "./Field";
import Input from "./Input";

function Room() {
  const { id } = useParams();

  const [error, setError] = useState(undefined);

  const [internalName, setInternalName] = useState("");
  const [area, setArea] = useState(0);
  const [location, setLocation] = useState("");
  const [publicName, setPublicName] = useState("");
  const [status, setStatus] = useState("");
  const [contractAddress, setContractAddress] = useState("");
  const [tenant, setTenant] = useState("");
  const [rentStart, setRentStart] = useState(0);
  const [rentEnd, setRentEnd] = useState(0);
  const [billingPeriod, setBillingPeriod] = useState(0);
  const [rentalRate, setRentalRate] = useState(0);
  const [editingPublicName, setEditingPublicName] = useState(false);

  const formatDate = (unixTime) => {
    const date = new Date(unixTime);
    return date.toUTCString();
  };

  const formatDuration = (unixTimeDuration) => {
    return unixTimeDuration;
  };

  // useEffect(async () => {
  // const contract = new web3.eth.Contract(
  //   RENTAL_ARGREEMENT_ABI,
  //   contractAddress
  // );
  // setStatus(STATUSES[await contract.methods.contractStatus().send()]);
  // setTenant(await contract.methods.getTenant().send());
  // setRentStart(await contract.methods.getRentStartTime().send());
  // setRentEnd(await contract.methods.getRentEndTime().send());
  // setBillingPeriod(await contract.methods.getBillingPeriodDuration().send());
  // setRentalRate(await contract.methods.getRentalRate().send());
  // }, [contractAddress]);

  // const { error: isError } = useQuery(GET_ROOM, {
  //   fetchPolicy: "no-cache",
  //   variables:     onCompleted: ({ data }) => {
  //     setInternalName(data.internalName);
  //     setArea(data.area);
  //     setLocation(data.location);
  //     setPublicName(data.publicName);
  //     setContractAddress(data.contractAddress);
  //     setStatus(STATUSES[data.status]);
  //     setTenant(data.tenantAddress);
  //     setRentStart(data.rentStart);
  //     setRentEnd(data.rentEnd);
  //     setBillingPeriod(data.billingPeriod);
  //     setRentalRate(data.rentalRate);
  //   },
  // });

  useEffect(async () => {
    gqlPost(GET_ROOM, {
      id: id,
    })
      .then((d) => {
        const data = d.data.room;
        console.log(data);
        setInternalName(data.internalName);
        setArea(data.area);
        setLocation(data.location);
        setPublicName(data.publicName);
        setContractAddress(data.contractAddress);
        setStatus(STATUSES[data.status]);
        setTenant(data.tenantAddress);
        setRentStart(data.rentStart);
        setRentEnd(data.rentEnd);
        setBillingPeriod(data.billingPeriod);
        setRentalRate(data.rentalRate);
      })
      .catch((e) => {
        setError(e);
      });
  }, []);

  const submitPublicName = async (e) => {
    e.preventDefault();
    setEditingPublicName(false);
    const res = await gqlPost(EDIT_PUBLIC_NAME, { id, publicName });
    console.log(res);
  };

  const doAllowRenting = async () => {
    console.log("allowRenting");
  };
  return (
    <>
      {!editingPublicName && <Field k="room__name" v={publicName} />}
      <Field k="room__internal-name" v={internalName} />
      <Field k="room__area" v={area} />
      <Field k="room__location" v={location} />
      <Field k="room__status" v={status} />
      <Field k="room__contract-address" v={contractAddress} />
      <Field k="room__tenant" v={tenant} />
      <Field k="room__rent-start" v={rentStart} f={formatDate} />
      <Field k="room__rent-end" v={rentEnd} f={formatDate} />
      <Field k="room__billing-period" v={billingPeriod} f={formatDuration} />
      <Field
        k="room__rental-rate"
        v={rentalRate}
        f={(rentalRate) => rentalRate.toString() + " wei"}
      />
      {isLandlord() && !editingPublicName && (
        <>
          <Button
            k="room__edit-public-name"
            onClick={() => setEditingPublicName(true)}
          />
          <Button k="room__allow-renting" onClick={doAllowRenting} />
        </>
      )}
      {editingPublicName && (
        <form className="public-name-edit">
          <Input
            k="public-name-edit__name"
            value={publicName ? publicName : undefined}
            cb={(e) => setPublicName(e.target.value)}
          />
          <Button
            type="submit"
            k="public-name-edit__submit"
            onClick={submitPublicName}
          />
        </form>
      )}
      {error && <p>Error: {error.toString()}</p>}
    </>
  );
}

export default Room;
