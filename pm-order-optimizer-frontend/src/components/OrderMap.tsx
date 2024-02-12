'use client'
import React from 'react'
import {GoogleMap, useJsApiLoader, Circle} from '@react-google-maps/api';
import {Point} from "@/types";


const center = {lat: -3.745, lng: -38.523}

function OrderMap({points, groupColors}: Readonly<{ points: Point[], groupColors: string[] }>) {
    const {isLoaded} = useJsApiLoader({
        id: 'google-map-script',
        googleMapsApiKey: process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY || ''
    })


    return isLoaded ? (
        <GoogleMap
            mapContainerStyle={{width: "100vh", height: '100vh'}}
            center={points.length > 0 ? {lat: points[0].lat, lng: points[0].lon} : center}
            zoom={16}
        >
            {
                points.map((point, index) => {
                    const color = groupColors[point.group]
                    return <Circle key={index} radius={4} center={{lat: point.lat, lng: point.lon}}
                                   options={{
                                       fillColor: color,
                                       strokeColor: color,
                                       fillOpacity: 1.0,
                                       strokeOpacity: 1.0
                                   }}/>
                })
            }
        </GoogleMap>
    ) : <></>
}

export default React.memo(OrderMap)