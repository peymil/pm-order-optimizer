// _app.jsx
import {
    QueryClient,
    QueryClientProvider,
} from '@tanstack/react-query'
import React from "react";

const queryClient = new QueryClient()

export default function RootLayout({Component, pageProps}: Readonly<{ Component: React.ComponentType, pageProps: any }>) {

    return (
        <QueryClientProvider client={queryClient}>
            <Component {...pageProps} />
        </QueryClientProvider>
    )
}