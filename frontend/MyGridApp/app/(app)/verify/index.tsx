import { MainText, Container, ShadowButton } from "@/components/widgets";
import { useLocalSearchParams, useRouter } from "expo-router";
import { checkVersion, getPushTokenAsync } from "@/utils";
import { useAuth } from "@/contexts/AuthContext";
import { registerPushToken } from "@/api/registerPushToken";
import { scopedI18n } from "@/translations/i18n";
import { Constants } from "@/theme";

export default function Verify () {

  const router = useRouter()
  const t = scopedI18n('verify')

  const { accessToken, user } = useAuth()
  const { maintenance, version } = useLocalSearchParams()

  console.log(maintenance, ' ', version)

  async function handlePress () {
    if (maintenance === 'true') {
      router.replace('/error/maintenance');
      return;
    }

    if (typeof version !== "string" || !checkVersion(version)) {
      router.replace('/error/update');
      return;
    }

    const pushToken = await getPushTokenAsync();
    try {
      if (pushToken) {
        await registerPushToken(accessToken, pushToken)
      }
    } catch (e) {
      console.log(e)
    }
    router.replace('/home')
  }

  return (
    <Container style={{ backgroundColor: 'transparent' }}>
      <MainText style={{ fontSize: Constants.fontSizes.big }}>{t('welcome')} {user.username}{t('!')}</MainText>
      <MainText>{t('weSent')}</MainText>
      <MainText>{t('verify')}</MainText>
      <ShadowButton onPress={handlePress}>{t('letsGo')}</ShadowButton>
    </Container>
  )
}