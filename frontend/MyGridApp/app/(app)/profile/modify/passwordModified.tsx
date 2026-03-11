import { Container, MainText } from "@/components/widgets";
import { useAuth } from "@/contexts/AuthContext";
import { Colors } from "@/theme";
import { scopedI18n } from "@/translations/i18n";
import { ActivityIndicator } from "react-native";

export default function PasswordModified () {

  const t = scopedI18n('profile.modify');
  const { logout } = useAuth();

  setTimeout(() => {
    logout();
  }, 5000)

  return (
    <Container style={{ backgroundColor: 'transparent' }}>
      <MainText fontSize="title" style={{ marginBottom: 44 }}>{t('passwordModified')}</MainText>
      <MainText style={{ maxWidth: '80%', marginBottom: 10 }}>{t('forSafety')}</MainText>
      <MainText style={{ maxWidth: '80%', marginBottom: 44 }}>{t('pleaseLogin')}</MainText>
      <ActivityIndicator color={Colors.light.lightText}/>
    </Container>
  )
}