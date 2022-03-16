import { useQuery } from "@apollo/client";
import { useParams } from "react-router-dom";
import { useState } from "react";

import { GET_ROOM } from "../gql/queries";
import { RENTAL_ARGREEMENT_ABI } from "../abi";

import Field from "./Field";

function Room() {
  const { id } = useParams();

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

  const formatDate = (unixTime) => {
    const date = new Date(unixTime);
    return date.toUTCString();
  };

  const formatDuration = (unixTimeDuration) => {
    return unixTimeDuration;
  };

  useEffect(async () => {
    const contract = new web3.eth.Contract(
      RENTAL_ARGREEMENT_ABI,
      contractAddress
    );
    const STATUSES = [
      "Unavailable for renting",
      "Rented",
      "Available for renting",
      "Rent ended",
    ];
    setStatus(STATUSES[await contract.methods.contractStatus().send()]);
    setTenant(await contract.methods.getTenant().send());
    setRentStart(await contract.methods.getRentStartTime().send());
    setRentEnd(await contract.methods.getRentEndTime().send());
    setBillingPeriod(await contract.methods.getBillingPeriodDuration().send());
    setRentalRate(await contract.methods.getRentalRate().send());
  }, [contractAddress]);

  const { error: isError } = useQuery(GET_ROOM, {
    fetchPolicy: "no-cache",
    variables: {
      id: id,
    },
    onCompleted: ({ data }) => {
      setInternalName(data.internalName);
      setArea(data.area);
      setLocation(data.location);
      setPublicName(data.publicName);
      setContractAddress(data.contractAddress);
    },
  });

  return (
    <>
      <Field k="room__name" v={publicName} />
      <Field k="room__internal-name" v={internalName} />
      <Field k="room__area" v={area} />
      <Field k="room__location" v={location} />
      <Field k="room__status" v={status} />
      <Field k="room__contract-address" v={contractAddress} />
      <Field k="room__tenant" v={tenant} />
      <Field k="room__rent-start" v={formatDate(rentStart)} />
      <Field k="room__rent-end" v={formatDate(rentEnd)} />
      <Field k="room__billing-period" v={formatDuration(billingPeriod)} />
      <Field k="room__rental-rate" v={toString(rentalRate) + " wei"} />
      {isError && <p>Error!</p>}
    </>
  );
}

export default Room;