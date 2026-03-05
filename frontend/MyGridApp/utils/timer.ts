import * as Localization from "expo-localization"
import { Interval, DateTime } from "luxon"

export function timer (datetime: string) {

  const interval = Interval.fromDateTimes(DateTime.now(), DateTime.fromISO(datetime)).toDuration([ 'days', 'hours', 'minutes', 'seconds', 'milliseconds' ]).toObject()
  const locale = Localization.getLocales()[0]?.languageCode || 'en';

  if (locale === 'fr') {
    return `${interval.days}j : ${interval.hours}h : ${interval.minutes}m : ${interval.seconds}s`
  }

  return `${interval.days}d : ${interval.hours}h : ${interval.minutes}m : ${interval.seconds}s`
}