"use client";

import { useEffect } from "react";
import { useApi } from "@/hooks";
import { useParams, useRouter } from "next/navigation";
import Image from "next/image";
import { SessionButton } from "@/components";

export default function Event () {
  
  const { id } = useParams();
  const router = useRouter();

  const { datas, error, loading, api: getEvents } = useApi();

  useEffect(() => {
    getEvents({ endpoint: `/api/nav/home/events/${id}` });
  }, []);

  return (
    <div className="container">
      {loading && <span></span>}
      {error && <h1>{error}</h1>}
      {datas && datas.event && <div>
        <h1 className="title">{datas.event.name}</h1>
        <div style={{ borderWidth: 1, borderStyle: 'solid', padding: 10, borderRadius: 4 }}>
          <p className="text"><b>id:</b> {datas.event.id}</p>
          <p className="text"><b>championship_id:</b> {datas.event.championship_id}</p>
          <div style={{ flexDirection: 'row', display: 'flex', alignItems: 'center', gap: 10  }}>
            <p className="text"><b>colors: </b></p>
            {datas.event.colors.map((color: string) => (
              <div key={color} style={{ flexDirection: 'row', display: 'flex', alignItems: 'center', gap: 10 }}>
                <div style={{ width: 20, height: 20, backgroundColor: color, borderWidth: 1, borderStyle: 'solid' }}></div>
                <p className="text">{color}</p>
              </div>
            ))}
          </div>
          <div style={{ flexDirection: 'row', display: 'flex', alignItems: 'center', gap: 10  }}>
            <p className="text"><b>flag:</b> {datas.event.flag} </p>
            <Image src={datas.event.flag} alt={datas.event.name + ' flag'} width={32} height={32}/>
          </div>
        </div>
        <div>
          <h1 className="header" style={{ marginTop: 40 }}>Sessions</h1>
          {datas.sessions.map((session: any) => (
            <SessionButton key={session.id} session={session}/>
          ))}
        </div>

      </div>}
    </div>
  )
}