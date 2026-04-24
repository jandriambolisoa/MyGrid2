"use client";

import { useEffect } from "react";
import { useApi } from "@/hooks";
import Image from 'next/image'
import { fromToDatetime } from "@/utils";
import { useRouter } from "next/navigation";

export default function Events () {

  const router = useRouter();

  const { datas, error, loading, api: getEvents } = useApi();

  useEffect(() => {
    getEvents({ endpoint: '/api/nav/home/events?championship_id=1', method: 'GET' });
  }, []);

  return (
    <div className="container">
      <h1 className="title">Events</h1>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
        {loading && <span></span>}
        {error && <h1>{error}</h1>}
        {datas && datas.events && datas.events.map((event: any) => (
          <button key={event.id} className="listButton" onClick={() => router.push(`/events/${event.id}`)}>
            <p className="header">{event.name}</p>
            <Image src={event.flag} alt={event.name + ' flag'} width={32} height={32}/>
            <p className="text">{fromToDatetime(event.datetime)}</p>
          </button>
        ))}
      </div>
    </div>
  )
}