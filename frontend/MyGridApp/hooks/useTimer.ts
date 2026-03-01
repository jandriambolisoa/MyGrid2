import { useState, useEffect } from "react"
import { timer } from "@/utils"

export function useTimer (datetime: string) {
  
  const [time, setTime] = useState(() => timer(datetime))

  useEffect(() => {
    const interval = setInterval(() => {
      setTime(timer(datetime))
    }, 1000)

    return () => clearInterval(interval);
  }, [datetime])

  return time

}