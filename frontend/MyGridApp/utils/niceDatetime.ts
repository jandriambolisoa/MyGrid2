import { DateTime } from "luxon"
import * as Localization from "expo-localization"
import { scopedI18n } from "@/translations/i18n"

export function niceDatetime (date: string): string {

  const t = scopedI18n('utils.niceDatetime')

  const locale = Localization.getLocales()[0]?.languageCode || 'en'

  const datetime = DateTime.fromISO(date).setLocale(locale) 

  if (locale === 'fr') {
    return (datetime.toFormat(`'${t('on')}' cccc '${t('at')}' HH'h'mm`))
  }

  return (datetime.toFormat(`'${t('on')}' cccc '${t('at')}' hh':'mm`))

}