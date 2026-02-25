import { Container, MainText, ShadowButton } from "@/components/widgets";
import { DateTime } from "luxon";
import { scopedI18n } from "@/translations/i18n";
import * as Localization from "expo-localization";
import { Image, View, ActivityIndicator } from "react-native";
import { Colors, Constants, GlobalStyles } from "@/theme";
import { useAuth } from "@/contexts/AuthContext";
import { useLogout } from "@/hooks";

export type ProfileProps = {
  tabBarHeight: number
}

export default function Profile ({
  tabBarHeight=0
}) {

  // temp profile picture
  const image = 'https://img2.51gt3.com/rac/racer/202503/cfc139b2b49e48cd80a436c00a71711d.png?x-oss-process=style/_nhd_en'

  const { user, logout } = useAuth();

  const locale = Localization.getLocales()[0]?.languageCode || 'en'
  const t = scopedI18n('home.profile')
  const { logout: backLogout, loading  } = useLogout();

  async function handleLogout () {
    const success = await backLogout();
    if (success) {
      logout();
    }
  }

  return (
    <Container style={{ justifyContent: 'space-between', paddingBottom: tabBarHeight }}>
      <View style={{ alignItems: 'center', marginTop: 50 }}>
        <MainText style={{ fontSize: 20 }}>{user?.username}</MainText>
        <Image style={GlobalStyles.profilePicture} source={{ uri: image }}/>
        <ShadowButton >
          <MainText>{t('editProfile')}</MainText>
        </ShadowButton>
        <ShadowButton style={{ marginTop: Constants.spacing.mainWidgetMargin}} onPress={handleLogout}>
          {loading ? <ActivityIndicator color={Colors.light.warning}/> : <MainText style={{ color: Colors.light.warning }}>{t('logout')}</MainText>}
        </ShadowButton>
      </ View>
      <MainText style={{ marginBottom: 20 }}>{DateTime.fromISO(user?.created || '').setLocale(locale).toFormat(`'${t('memberSince')}' d MMMM yyyy`)}</MainText>
    </Container>
  )
}