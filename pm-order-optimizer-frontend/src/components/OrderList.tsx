import {Order, Point} from "@/types";
import _ from "lodash"
import React from "react";

const OrderList = ({orders, groupColors}: { orders: Order[], groupColors: string[] }) => {
    const groupedOrders = React.useMemo(() => {
        return Object.entries(_.groupBy(orders, 'group'))
    }, [orders])
    return (
        <div className={"overflow-y-auto"}>
            <h1>Points</h1>
            <ul className={"h-svh"}>
                {groupedOrders.map(([group, orders], index) => {
                    const ordersList = orders.map(order => {
                        return <>
                            <li>id: {order.id}</li>
                            <li key={index}>{order.lat}, {order.lon}</li>
                            <li>address: {order.address}</li>
                        </>
                    })
                    return <>
                        <li style={{color: groupColors[index]}}>Group {group}
                            <ul key={index} style={{color: groupColors[index]}}>
                                {...ordersList}
                            </ul>
                        </li>
                    </>
                })}
            </ul>
        </div>
    )
}

export default React.memo(OrderList)