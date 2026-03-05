import { Container, MainText } from "@/components/widgets";
import { Colors, Constants } from "@/theme";
import { scopedI18n } from "@/translations/i18n";
import { FontAwesome6 } from "@expo/vector-icons";
import { View } from "react-native";

export default function Social () {

  const t = scopedI18n('home.social')

  return (
    <Container style={{ backgroundColor: 'transparent' }}>
      <View style={{ height: '80%', alignSelf: 'stretch', justifyContent: 'center', alignItems: 'center' }}>
        <FontAwesome6 name='gears' color={Colors.light.lightText} size={30}/>
        <MainText style={{ fontSize: Constants.fontSizes.header, marginVertical: 16 }} bold={true}>{t('wip')}</MainText>
        <MainText style={{ maxWidth: '80%' }}>{t('stayTuned')}</MainText>
      </View>
    </Container>
  )
}