import { Container } from "@/components/widgets/Container";
import { MainText } from "@/components/widgets/MainText";
import { TouchableOpacity } from "react-native";
import { AntDesign } from "@expo/vector-icons";
import { scopedI18n } from "@/translations/i18n";

const t = scopedI18n('auth.login')

export default function Login () {

  function handleGoogle () {

  }

  return (
    <Container style={{ justifyContent: 'center', alignItems: 'center'}}>
      <TouchableOpacity onPress={handleGoogle} style={{borderWidth: 1, borderColor: 'white', padding: 10, borderRadius: 4, flexDirection: 'row'}}>
        <MainText>{t('signInGoogle')}</MainText>
        <AntDesign name="google" size={18} color="white" style={{ marginLeft: 8 }} />
      </TouchableOpacity>
      <TouchableOpacity onPress={handleGoogle} style={{borderWidth: 1, borderColor: 'white', padding: 10, borderRadius: 4, marginTop: 18, flexDirection: 'row'}}>
        <MainText>{t('signInApple')}</MainText>
        <AntDesign name="apple" size={18} color="white" style={{ marginLeft: 8}} />
      </TouchableOpacity>
    </Container>
  )
}