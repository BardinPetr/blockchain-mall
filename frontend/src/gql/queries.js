import { gql } from "@apollo/client";

export const AUTHENTICATION = gql`
  query {
    authentication {
      address
      isLandlord
    }
  }
`;

export const GET_ROOM = gql`
  query ($id: String) {
    rooms(id: $id) {
      internalName
      area
      location
      publicName
      contractAddress
    }
  }
`;

export const GET_TENANT_ROOMS = gql`
  query($address: String) {
    rooms()
  }
`;

export const GET_ALL_ROOMS = gql`
  query {
    rooms {
      id
      publicName
    }
  }
`;

export const STATUSES = {
  0: "Unavailable for renting",
  1: "Rented",
  2: "Available for renting",
  3: "Rent ended",
  UNAVAILABLE: 0,
  RENTED: 1,
  AVAILABLE: 2,
  ENDED: 2,
};
