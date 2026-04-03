"use client";

import Image from "next/image";
import { useApi } from "@/hooks";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export default function SendNotification () {

  const router = useRouter();

  const { error: error, loading, api: sendNotification } = useApi();

  const [errorMsg, setErrorMsg] = useState("");
  const [enTitle, setEnTitle] = useState("");
  const [enBody, setEnBody] = useState("");
  const [frTitle, setFrTitle] = useState("");
  const [frBody, setFrBody] = useState("");

  useEffect(() => {
    if (error) {
      setErrorMsg(error);
    }
  })

  async function handleSend () {

    setErrorMsg("");

    if (!enTitle || !enBody || !frTitle || !frBody) {
      setErrorMsg("Please fill all fields");
      return;
    }

    const success = await sendNotification({
      endpoint: '/api/manager/notification/push/send',
      method: 'POST',
      body: {
        title: {
          en: enTitle,
          fr: frTitle
        },
        body: {
          en: enBody,
          fr: frBody
        }
      }
    });
    if (success) {
      router.back();
    }
  }

  return (
    <div className="container">
      <h1 className="title">Send notification</h1>
      <p style={{ fontSize: '0.875rem' }}>This page will send a notification to every user</p>
      <div style={{ borderWidth: 1, borderStyle: 'solid', padding: 10, paddingBottom: 0, borderRadius: 4, display: 'flex', flexDirection: 'column', marginTop: 20, alignItems: 'center' }}>
        <Image style={{ marginBottom: 10 }} src={"https://flagsapi.com/GB/flat/64.png"} alt={"English language flag"} width={32} height={32}/>
        <input className="input" placeholder="Title en" value={enTitle} onChange={(e) => setEnTitle(e.target.value)} />
        <textarea className="input" placeholder="Body en" style={{ width: '90%' }} rows={4} value={enBody} onChange={(e) => setEnBody(e.target.value)}/>
      </div>
      <div style={{ borderWidth: 1, borderStyle: 'solid', padding: 10, paddingBottom: 0, borderRadius: 4, display: 'flex', flexDirection: 'column', marginTop: 20, alignItems: 'center' }}>
        <Image style={{ marginBottom: 10 }} src={"https://flagsapi.com/FR/flat/64.png"} alt={"French language flag"} width={32} height={32}/>
        <input className="input" placeholder="Title fr" value={frTitle} onChange={(e) => setFrTitle(e.target.value)} />
        <textarea className="input" placeholder="Body fr" style={{ width: '90%' }} rows={4} value={frBody} onChange={(e) => setFrBody(e.target.value)}/>
      </div>
      {errorMsg && <p style={{ color: 'red', marginTop: 40, marginBottom: 0 }}>{errorMsg}</p>}
      <button className="button" style={{ cursor: 'pointer', marginTop: 40, marginBottom: 40 }} onClick={handleSend} disabled={loading}>
          {loading ? (
            "Loading..."
          ) : (
            "Send notification"
          )}
      </button>
    </div>
  )
}