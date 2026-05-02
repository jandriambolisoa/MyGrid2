"use client";

import { useParams, useRouter } from "next/navigation";
import { useApi } from "@/hooks";
import { useEffect, useState } from "react";
import { DragDropProvider } from "@dnd-kit/react";
import { SortableDriver } from "@/components";
import { isSortable } from "@dnd-kit/react/sortable";

export default function SessionRegistrations () {

  const router = useRouter();

  const { id } = useParams();
  const { datas, api: getDrivers } = useApi(true);
  const { error: sendError, loading: sendLoading, api: sendRegistrations } = useApi();

  const [drivers, setDrivers] = useState([]);

  useEffect(() => {
    getDrivers({
      endpoint: `/api/events/sessions/registrations/${id}`
    })
  }, [])

  useEffect(() => {
    if (datas?.registrations) {
      setDrivers(datas.registrations)
    }
  }, [datas])

  async function handleRegistrations () {

    const makeList = drivers.map((item: any, index: number) => {
      return {
        driver_id: item.driver.id,
        team_id: item.team.id,
        prediction: index + 1
      }
    })

    const success = await sendRegistrations({
      endpoint: `/api/events/sessions/registrations/${id}`,
      body: makeList,
      method: 'POST'
    })

    if (success) {
      router.back();
    }
    return

  }

  return (
    <div className="container">
      <h1 className="title">Session registrations</h1>
      {drivers.length && <div style={{ display: 'flex', flexDirection: 'row', gap: 10}}>
        <ul>
          {drivers.map((item, index) => 
            <li key={index}>
              {index + 1}
            </li>
          )}
        </ul>
        <DragDropProvider
          onDragEnd={(event) => {

            if (event.canceled) return;

            const {source} = event.operation;

            if (isSortable(source)) {
              const {initialIndex, index} = source;

              setTimeout(() => {if (initialIndex !== index) {
                setDrivers((items) => {
                  const newItems = [...items];
                  const [removed] = newItems.splice(initialIndex, 1);
                  newItems.splice(index, 0, removed);
                  return newItems;
                });
              }}, 300);
            }
          }}
        >
          <ul>
            {drivers.map((item, index) => 
              <SortableDriver key={item.driver.id} item={item} index={index}/>
            )}
          </ul>
        </DragDropProvider>
      </div>}
      {sendError && <p style={{ color: 'red', marginTop: 40, marginBottom: 0 }}>{sendError}</p>}
      <button className="button" style={{ cursor: 'pointer', marginTop: 40, marginBottom: 40 }} onClick={handleRegistrations} disabled={sendLoading}>
          {sendLoading ? (
            "Loading..."
          ) : (
            "Send registrations"
          )}
      </button>
    </div>
  )
}