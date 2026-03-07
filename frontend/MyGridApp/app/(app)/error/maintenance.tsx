import { Container, MainText, ShadowButton } from "@/components/widgets"
import { Constants } from "@/theme"
import { scopedI18n } from "@/translations/i18n"
import { View, Platform, Linking } from "react-native"

export default function Maintenance () {

  const t = scopedI18n('error.maintenance')

  return (
    <Container style={{ backgroundColor: 'transparent' }}>
      <View style={{ width: '80%' }}>
        <MainText style={{ fontSize: Constants.fontSizes.title, marginBottom: 40 }}>{t('back')}</MainText>
        <MainText>{t('maintenance')}</MainText>
      </View>
    </Container>
  )
}