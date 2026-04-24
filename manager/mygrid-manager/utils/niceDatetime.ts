import { DateTime } from "luxon"

export function niceDatetime (date: string, weekDay: boolean = true): string {

  const datetime = DateTime.fromISO(date)

  if (weekDay) {
    return datetime.toFormat(`'On' cccc 'at' hh':'mm a`)
  }

  return datetime.toFormat(`'On' MMMM d 'at' hh':'mm a`)
}