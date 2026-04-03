"use client";

import { niceDatetime } from "@/utils"
import { useRouter } from "next/navigation";
import { useState } from "react";
import { DateTime } from "luxon";

export function SessionButton ({ session }: { session: any }) {

  const router = useRouter();

  const [picked, setPicked] = useState(false);

  const resultLabel = session.is_over ? 'Edit results' : 'Add results';

  return (
    <div className="listElement" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between', alignItems: 'center' }}>
      <div style={{ display: 'flex', flexDirection: 'row', backgroundColor: 'transparent', alignSelf: 'stretch', justifyContent: 'space-between', alignItems: 'center' }} onClick={() => setPicked(!picked)}>
        <p className="text"><b>{session.name}</b></p>
        <p className="text">{niceDatetime(session.datetime)}</p>
      </div>
      {picked && <div style={{ alignSelf: 'stretch', gap: 10, display: 'flex', flexDirection: 'column', marginTop: 10 }}>
        {DateTime.fromISO(session.datetime) > DateTime.now() && <button className="listButton" style={{ color: 'white', alignSelf: 'stretch', margin: 0 }} onClick={() => router.push(`/session/${session.id}/registrations`)}>
          Change registrations
        </button>}
        {DateTime.fromISO(session.datetime) < DateTime.now() && <button className="listButton" style={{ color: 'white', alignSelf: 'stretch', margin: 0 }} onClick={() => router.push(`/session/${session.id}/results?results=${session.is_over}`)}>
          {resultLabel}
        </button>}
      </div>}
    </div>
  )
}