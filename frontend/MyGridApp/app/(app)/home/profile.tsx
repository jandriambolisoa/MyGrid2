import { Container, MainText, ShadowButton, ProfilePicture } from "@/components/widgets";
import { DateTime } from "luxon";
import { scopedI18n } from "@/translations/i18n";
import * as Localization from "expo-localization";
import { View, ActivityIndicator } from "react-native";
import { Colors, Constants } from "@/theme";
import { useAuth } from "@/contexts/AuthContext";
import { useLogout } from "@/hooks";
import { useRouter } from "expo-router";
import { useToast } from "@/contexts/ToastContext";

export type ProfileProps = {
  tabBarHeight: number
}

export default function Profile ({
  tabBarHeight=0
}) {

  const router = useRouter();
  const locale = Localization.getLocales()[0]?.languageCode || 'en';
  const t = scopedI18n('home.profile');

  const { user, logout } = useAuth();
  const { logout: backLogout, loading  } = useLogout();

  async function handleLogout () {
    const success = await backLogout();
    if (success) {
      logout();
    }
  }

  function handleModify () {
    router.push('/profile/modify')
  }

  return (
    <Container style={{ justifyContent: 'space-between', paddingBottom: tabBarHeight, backgroundColor: 'transparent' }}>
      <View style={{ alignItems: 'center', marginTop: 50, alignSelf: 'stretch' }}>
        <MainText style={{ fontSize: Constants.fontSizes.title }}>{user?.username}</MainText>
        <ProfilePicture link={user?.image_url} borders={true} size={150} style={{ marginVertical: 36 }}/>
        <ShadowButton style={{ minWidth: Constants.spacing.profileButtonWidth as any }} onPress={handleModify}>
          <MainText>{t('editProfile')}</MainText>
        </ShadowButton>
        <ShadowButton style={{ marginTop: Constants.spacing.mainWidgetMargin, minWidth: Constants.spacing.profileButtonWidth as any }} onPress={handleLogout}>
          {loading ? <ActivityIndicator color={Colors.light.warning}/> : <MainText style={{ color: Colors.light.warning }}>{t('logout')}</MainText>}
        </ShadowButton>
      </ View>
      <MainText style={{ marginBottom: Constants.spacing.mainWidgetMargin }}>{DateTime.fromISO(user?.created || '').setLocale(locale).toFormat(`'${t('memberSince')}' d MMMM yyyy`)}</MainText>
    </Container>
  )
}