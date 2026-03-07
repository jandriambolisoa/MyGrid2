import * as Localization from 'expo-localization';

export function rankNumber (rank: number) {

  const locale = Localization.getLocales()[0].languageCode || 'en';

  if (locale === 'fr') {
    if (rank === 1) {
      return String(rank) + 'er';
    }
    return String(rank) + 'ème';
  }
  if (Math.floor(rank / 10) % 10 === 1) {
    return String(rank) + 'th';
  }
  switch (rank % 10) {
    case 1:
      return String(rank) + 'st';

    case 2:
      return String(rank) + 'nd';

    case 3:
      return String(rank) + 'rd';

    default:
      return String(rank) + 'th';
  }
}