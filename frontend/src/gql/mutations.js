import { gql } from "@apollo/client";

export const REQUEST_AUTHENTICATION = gql`
  mutation RequestAuthentication($address: String!) {
    message: requestAuthentication(address: $address)
  }
`;

export const AUTHENTICATE = gql`
    mutation Authenticate($address: String!, $v: String!, $r: String!, $s: String!) {
        authentication: authenticate(
            address: $address
            signedMessage: {
                v: $v,
                r: $r,
                s: $s
            }
        ) {
            address
            isLandlord
        }
    }
`;

export const CREATE_ROOM = gql`
  mutation CreateRoom($room: InputRoom!) {
    createRoom(room: $room) {
      id
    }
  }
`;
