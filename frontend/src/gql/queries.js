import { gql } from "@apollo/client";

export const AUTHENTICATION = gql`
    query {
        authentication { address, isLandlord }
    }
`;

