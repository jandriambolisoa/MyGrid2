import * as Localization from "expo-localization";

const locale = Localization.getLocales()?.[0].languageCode || 'en';

export function userScore (username: string) {

    if (locale === 'fr') {
      return `Score de ${username}`
    }

    return `${username}'s Score`
  }