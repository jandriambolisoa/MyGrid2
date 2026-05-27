import { DateTime } from 'luxon';

export function fromToDatetime (date: string): string {

  const end = DateTime.fromISO(date)
  const start = end.minus({ days: 2 })

  if (end.month === start.month) {
    return `From ${start.toFormat('MMMM dd')} to ${end.toFormat('dd')}`
  }

  return `From ${start.toFormat('MMMM dd')} to ${end.toFormat('MMMM dd')}`

}