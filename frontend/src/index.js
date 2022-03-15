import React from "react";
import ReactDOM from "react-dom";
import {ApolloClient, ApolloProvider, createHttpLink, InMemoryCache} from "@apollo/client";

import App from "./App";

const DEBUG = false;

const httpLink = createHttpLink({
    uri: `${DEBUG ? "http://0.0.0.0:8089" : window.location.origin}/graphql`,
    credentials: 'same-origin'
});

const client = new ApolloClient({
    uri: httpLink,
    cache: new InMemoryCache(),
});

ReactDOM.render(
    <React.StrictMode>
        <ApolloProvider client={client}>
            <App/>
        </ApolloProvider>
    </React.StrictMode>,
    document.getElementById("root")
);
