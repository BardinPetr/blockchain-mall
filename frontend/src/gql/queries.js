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
  query ($id: ID!) {
    room(id: $id) {
      internalName
      area
      location
      publicName
      contractAddress
      isAvailableForRent
      status
      tenant
      rentStart
      rentEnd
      billingPeriod
      rentalRate
    }
  }
`;

export const GET_ROOM_FOR_EDIT = gql`
  query ($id: ID!) {
    room(id: $id) {
      internalName
      area
      location
    }
  }
`;

export const GET_TENANT_ROOMS = gql`
  query ($address: String) {
    rooms(tenantAddress: $address) {
      id
      publicName
      status
    }
  }
`;

export const GET_ALL_ROOMS = gql`
  query {
    rooms {
      id
      publicName
      status
    }
  }
`;

export const GET_RPC_URL = gql`
  query {
    getRpcUrl
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
