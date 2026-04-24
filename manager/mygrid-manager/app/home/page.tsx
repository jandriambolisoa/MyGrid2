"use client"

import { useRouter } from "next/navigation";

export default function Home () {

  const router = useRouter();

  return (
    <div className="container">
      <h1 className="title">MyGrid Manager</h1>
      <div className="homeCategory">
        <h1 className="label">Events</h1>
        <button className="homeButton" onClick={() => router.push('/events')}>See events</button>
        <button className="homeButton" style={{ opacity: 0.5 }} disabled={true}>Update predictions</button>
        <h1 className="label">Notifications</h1>
        <button className="homeButton" onClick={() => router.push('/notification/send')}>Send notification</button>
        <button className="homeButton" style={{ opacity: 0.5 }} disabled={true}>Send mail</button>
      </div>
    </div>
  )
}