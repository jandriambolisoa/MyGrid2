import { Container, MainText } from "@/components/widgets";
import { scopedI18n } from "@/translations/i18n";
import { View } from "react-native";

export default function ServerError () {

  const t = scopedI18n('serverError')

  return (
    <Container style={{ backgroundColor: 'transparent' }}>
      <View style={{ width: '80%' }}>
        <MainText fontSize='title'>{t('oops')}</MainText>
        <MainText style={{ marginBottom: 20, marginTop: 44 }}>{t('something')}</MainText>
        <MainText>{t('please')}</MainText>
      </View>
    </Container>
  )
}