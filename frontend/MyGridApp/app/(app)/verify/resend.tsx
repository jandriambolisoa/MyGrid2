import { Container, MainText, ShadowButton } from "@/components/widgets";
import { Colors, Constants } from "@/theme";
import { scopedI18n } from "@/translations/i18n";
import { ActivityIndicator, View } from 'react-native'
import { useApi } from "@/hooks";
import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "expo-router";

export default function Resend () {

  const t = scopedI18n('verify.resend');
  const auth = useAuth()
  const router = useRouter()

  const { loading, api: resendEmail } = useApi()

  async function handlePress () {
    const success = await resendEmail({
      endpoint: '/users/send-verification-email',
      method: 'GET',
      auth: auth
    })
    if (success) {
      router.push('/home')
    }
  }

  return (
    <Container style={{ backgroundColor: 'transparent' }}>
      <View style={{ maxWidth: '80%' }}>
        <MainText style={{ fontSize: Constants.fontSizes.title }}>{t('yourAccount')}</MainText>
        <MainText style={{ marginVertical: 44 }}>{t('youNeed')}</MainText>
        <ShadowButton onPress={handlePress}>
          {loading ? <ActivityIndicator color={Colors.light.lightText}/> : <MainText>{t('resend')}</MainText>}
        </ShadowButton>
      </View>
    </Container>
  )
}