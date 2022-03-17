import { gql } from "@apollo/client";

export const REQUEST_AUTHENTICATION = gql`
  mutation RequestAuthentication($address: String!) {
    message: requestAuthentication(address: $address)
  }
`;

export const AUTHENTICATE = gql`
  mutation Authenticate(
    $address: String!
    $v: String!
    $r: String!
    $s: String!
  ) {
    authentication: authenticate(
      address: $address
      signedMessage: { v: $v, r: $r, s: $s }
    ) {
      address
      isLandlord
    }
  }
`;

export const GET_ACCESS_TOKEN = gql`
  mutation GetAccessToken($address: String!) {
    token: getAccessToken(address: $address)
  }
`;

export const CREATE_ROOM = gql`
  mutation CreateRoom($room: InputRoom!) {
    createRoom(room: $room) {
      id
    }
  }
`;

export const EDIT_ROOM = gql`
  mutation EditRoom(
    $id: ID!
    $internalName: String!
    $area: Float!
    $location: String!
  ) {
    editRoom(
      id: $id
      room: { internalName: $internalName, area: $area, location: $location }
    ) {
      id
    }
  }
`;

export const EDIT_PUBLIC_NAME = gql`
  mutation EditPublicName($id: ID!, $publicName: String!) {
    setRoomPublicName(id: $id, publicName: $publicName) {
      id
    }
  }
`;
