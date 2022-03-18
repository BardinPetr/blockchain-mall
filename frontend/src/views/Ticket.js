import {useEffect, useState} from "react";
import {gqlPost} from "../tools/tools";
import {useParams} from "react-router-dom";
import {GET_TICKET} from "../gql/queries";

function Ticket() {
    const {id} = useParams();
    const [ticket, setTicket] = useState(undefined);
    // const [newAddress, setNewAddress] = useState("");

    useEffect(async () => {
        const d = (await gqlPost(GET_TICKET, {id}));
        console.log(d);
        setTicket(d.data.ticket);
    }, []);

    // const sumbitCashier = async () => {
    //     const d = await gqlPost(ADD_CASHIER, {id, address: newAddress});
    //     console.log(d);
    // }

    return (
        <>
            <p>ticket</p>
            {ticket && (
                <>
                    <p className="ticket__store">{ticket.room.publicName || ticket.room.internalName}</p>
                    <p className="ticket__value">{ticket.value.wei} wei</p>
                    <p className="ticket__deadline">{ticket.deadline.beautiful}</p>
                </>
            )}
            {/*<form className="add-cashier" onSubmit={sumbitCashier}>*/}
            {/*    <Input*/}
            {/*        type="text"*/}
            {/*        k="add-cashier__address"*/}
            {/*        onInput={(e) => setNewAddress(e.target.value)}*/}
            {/*        value={newAddress}*/}
            {/*        required*/}
            {/*    />*/}
            {/*    <Button type="submit" k="add_cashier__submit"/>*/}
            {/*</form>*/}
        </>
    );
}

export default Ticket;
