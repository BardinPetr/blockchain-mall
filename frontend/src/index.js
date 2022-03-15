import React from "react";
import ReactDOM from "react-dom";
import {ApolloClient, ApolloProvider, InMemoryCache} from "@apollo/client";

import App from "./App";

const DEBUG = true;

const client = new ApolloClient({
    uri: `${DEBUG ? "http://0.0.0.0:8089" : window.location.origin}/graphql`,
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
