import { DateTime } from 'luxon';
import { scopedI18n } from '@/translations/i18n';
import * as Localization from 'expo-localization';

export function fromToDatetime (date: string): string {

  const t = scopedI18n('utils.fromToDatetime')

  const locale = Localization.getLocales()[0]?.languageCode || 'en'

  const end = DateTime.fromISO(date).setLocale(locale)
  const start = end.minus({ days: 2 })

  if (locale === 'fr') {
    return `${t('from')} ${start.toFormat('dd MMMM')} ${t('to')} ${end.toFormat('dd MMMM')}`
  }

  return `${t('from')} ${start.toFormat('MMMM dd')} ${t('to')} ${end.toFormat('MMMM dd')}`

}