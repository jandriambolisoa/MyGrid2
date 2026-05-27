"use client";

import { useApi } from "@/hooks/useApi";
import { useParams, useSearchParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { isSortable } from "@dnd-kit/react/sortable";
import { DragDropProvider } from "@dnd-kit/react";
import { SortableDriver } from "@/components";

export default function SessionResults () {

  const router = useRouter();

  const { id } = useParams();
  const searchParams = useSearchParams();
  const results = searchParams.get('results');

  const { datas, api: getDrivers } = useApi(true);
  const { error: sendError, loading: sendLoading, api: sendResults } = useApi();

  const [drivers, setDrivers] = useState([]);
  const [chosenType, setChosenType] = useState({type: "None", points: []});

  const pointsTypes = [
    {type: "Race", points: [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]}, 
    {type: "Sprint", points: [8, 7, 6, 5, 4, 3, 2, 1]}, 
    {type: "None", points: []}
  ];

  useEffect(() => {
    getDrivers({
      endpoint: results === 'true' ? `/api/events/sessions/results/${id}` : `/api/events/sessions/registrations/${id}`
    })
  }, [])

  useEffect(() => {
    if (datas) {
      if (results === 'true') {
        setDrivers(datas.results);
        return;
      }
      setDrivers(datas.registrations);
    }
  }, [datas])

  async function handleResults () {

    const makeList = drivers.map((item: any, index: number) => {
      return {
        driver_id: item.driver.id,
        result: index + 1,
        points: chosenType.points[index] || 0
      }
    })

    const success = await sendResults({
      endpoint: `/api/events/sessions/results/${id}`,
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
      <h1 className="title">Session results</h1>
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
        <ul>
          {chosenType.points.map((item, index) => 
            <li key={index}>
              + {item}
            </li>
          )}
        </ul>
      </div>}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
        <p><b>Point system:</b></p>
        {pointsTypes.map((item) => (
          <label key={item.type}>
            <input type="radio" name="points" value={item.type.toLowerCase()} checked={chosenType.type === item.type} onChange={() => setChosenType(item)}/>
            {item.type}
          </label>
        ))}
        {/*<label style={{ marginTop: 20}}>
          <input type="checkbox" onChange={() => {
            setHalf(!half)
          }}/>
          50% points
        </label>*/}
      </div>
      {sendError && <p style={{ color: 'red', marginTop: 40, marginBottom: 0 }}>{sendError}</p>}
      <button className="button" style={{ cursor: 'pointer', marginTop: 40, marginBottom: 40 }} onClick={handleResults} disabled={sendLoading}>
        {sendLoading ? (
          "Loading..."
        ) : (
          "Send results"
        )}
      </button>
    </div>
  )
}