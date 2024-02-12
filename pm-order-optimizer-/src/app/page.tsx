'use client'
import React, {useMemo} from 'react'
import OrderMap from "@/components/OrderMap";
import {useQuery} from "@tanstack/react-query";
import axios from "axios";
import {base_url} from "@/constant";
import {getRandomColor} from "@/utils/getRandomColor";
import {Order} from "@/types";
import OrderList from "@/components/OrderList";

const containerStyle = {
    width: '400px',
    height: '400px'
};

const center = {
    lat: -3.745,
    lng: -38.523
};

function Page() {
    const {status, data, error, isFetching, refetch} = useQuery<Order[]>({
        queryKey: ['orders'],
        queryFn: () => {
            return axios.get(`${base_url}/orders/`).then(response => response.data)
        }
    })

    async function groupPositions(formData: FormData) {
        const group_count = formData.get("groupCount");
        const algorithm = formData.get("algorithm");
        if (!group_count || !algorithm) {
            alert("Please fill in all fields");
            return;
        }
        await axios.post(`${base_url}/orders/group`, {group_count, algorithm})
        await refetch()
    }

    async function seedPositions(formData: FormData) {
        const count = formData.get("count");
        if (!count) {
            alert("Please fill in all fields");
            return;
        }
        await axios.post(`${base_url}/orders/seed`, {count})
        await refetch()
    }

    async function reverseGeocodeAll(formData: FormData) {
        await axios.post(`${base_url}/orders/reverse-geocode`)
        await refetch()
    }

    async function deleteAllPositions() {
        await axios.delete(`${base_url}/orders`)
        await refetch()
    }

    const groupColors = useMemo(() => {
        if (!data) return []
        const groups = data.map(point => point.group)
        const uniqueGroups = Array.from(new Set(groups))
        return uniqueGroups.map(group => getRandomColor())
    }, [data])
    return (
        <>
            <main className="flex min-h-screen flex-col items-center justify-between bg-black">
                <div className={"flex flex-row justify-evenly"}>
                    {
                        isFetching ? <p>Loading...</p> :
                            <>
                                <OrderMap points={data || []} groupColors={groupColors}/>
                                <OrderList orders={data || []} groupColors={groupColors}/>
                            </>
                    }
                </div>

                <div className={"flex flex-col w-full space-y-4"}>
                    <form action={groupPositions} className={"flex space-x-4 justify-center flex-row"}>
                        <label htmlFor="groupCount">Group Count</label>
                        <input name="groupCount" type={"number"} defaultValue={20} className={"text-black"}/>
                        <select name={"algorithm"} className={"text-black"}>
                            <option>kmeans-constrained</option>
                            <option>kmeans</option>
                        </select>
                        <button type="submit" className={"bg-white text-black"}>Group Positions</button>
                    </form>

                    <form action={seedPositions} className={"flex space-x-4 justify-center flex-row"}>
                        <label htmlFor="count">Position Count</label>
                        <input name="count" type={"number"} defaultValue={500} className={"text-black"}/>
                        <button type="submit" className={"bg-white text-black"}>Seed Positions</button>
                    </form>

                    <form action={reverseGeocodeAll} className={"flex space-x-4 justify-center flex-row"}>
                        <button type="submit" className={"bg-white text-black "}>Reverse Geocode</button>
                    </form>

                    <form action={deleteAllPositions} className={"flex space-x-4 justify-center flex-row"}>
                        <button type="submit" className={"bg-white text-black "}>Delete All Positions</button>
                    </form>
                </div>
            </main>
        </>
    )
}

export default React.memo(Page)