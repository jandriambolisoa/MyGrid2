import { MainText, Container, ShadowButton } from "@/components/widgets";
import { useLocalSearchParams, useRouter } from "expo-router";
import { checkVersion, getPushTokenAsync } from "@/utils";
import { useAuth } from "@/contexts/AuthContext";
import { registerPushToken } from "@/api/registerPushToken";
import { scopedI18n } from "@/translations/i18n";
import { Colors, Constants } from "@/theme";
import { ActivityIndicator, View } from 'react-native';
import { useState } from "react";
 
export default function Verify () {

  const router = useRouter()
  const t = scopedI18n('verify')

  const { accessToken, user } = useAuth()
  const { maintenance, version } = useLocalSearchParams()

  const [loading, setLoading] = useState(false)

  async function handlePress () {

    setLoading(true)

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

  function buttonContent () {
    if (loading) {
      return <ActivityIndicator color={Colors.light.lightText}/>
    }
    return <MainText>{t('letsGo')}</MainText>
  }

  return (
    <Container style={{ backgroundColor: 'transparent' }}>
      <View style={{ width: '80%' }}>
        <MainText style={{ fontSize: Constants.fontSizes.title, marginBottom: 44 }}>{t('welcome')} {user.username}{t('!')}</MainText>
        <MainText style={{ marginBottom: 10 }}>{t('weSent')}</MainText>
        <MainText>{t('verify')}</MainText>
        <ShadowButton onPress={handlePress} style={{ marginTop: 44, width: '80%', alignSelf: 'center' }}>
          {buttonContent()}
        </ShadowButton>
      </View>
    </Container>
  )
}