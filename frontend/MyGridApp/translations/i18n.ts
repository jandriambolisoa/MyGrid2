import * as Localization from 'expo-localization';
import { I18n } from 'i18n-js';

// Import your translations
import en from '@/translations/en.json'
import fr from '@/translations/fr.json'

// Set translations
const i18n = new I18n({
  en,
  fr,
});

// Set the locale based on the device
//i18n.locale = Localization.getLocales();
i18n.locale = Localization.getLocales()[0]?.languageCode || 'en'

// Set the default fallback language
i18n.defaultLocale = 'en';

// Enable fallback to the defaultLocale
i18n.enableFallback = true

export const scopedI18n = (basePath: string) => (key: string, options = {}) => i18n.t(`${basePath}.${key}`, options)

export default i18n;