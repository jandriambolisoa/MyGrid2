import { Container, MainText, ShadowButton } from "@/components/widgets";
import { DateTime } from "luxon";
import { scopedI18n } from "@/translations/i18n";
import * as Localization from "expo-localization";
import { Image, View } from "react-native";
import { GlobalStyles } from "@/theme";

export type ProfileProps = {
  tabBarHeight: number
}

export default function Profile ({
  tabBarHeight=0
}) {

  // Temp strings to test layout
  const pseudo = "Norris_2026";
  const time = "2025-04-25T03:41:44.092651+01:00"

  const locale = Localization.getLocales()[0]?.languageCode || 'en'
  const t = scopedI18n('home.profile')

  return (
    <Container style={{ justifyContent: 'space-between', paddingBottom: tabBarHeight }}>
      <View style={{ alignItems: 'center', marginTop: 50 }}>
        <MainText style={{ fontSize: 20 }}>{pseudo}</MainText>
        <Image style={GlobalStyles.profilePicture} source={{ uri: 'https://img2.51gt3.com/rac/racer/202503/cfc139b2b49e48cd80a436c00a71711d.png?x-oss-process=style/_nhd_en' }}/>
        <ShadowButton >
          <MainText>{t('editProfile')}</MainText>
        </ShadowButton>
      </ View>
      <MainText style={{ marginBottom: 20 }}>{DateTime.fromISO(time).setLocale(locale).toFormat(`'${t('memberSince')}' d MMMM yyyy`)}</MainText>
    </Container>
  )
}