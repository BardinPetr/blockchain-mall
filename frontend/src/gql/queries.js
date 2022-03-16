import { gql } from "@apollo/client";

export const AUTHENTICATION = gql`
    query {
        authentication { address, isLandlord }
    }
`;

export const GET_ROOM = gql`
  query($id: String) {
    rooms(id: $id) {
      internalName
      area
      location
      publicName
      contractAddress
    }
  }
`;
