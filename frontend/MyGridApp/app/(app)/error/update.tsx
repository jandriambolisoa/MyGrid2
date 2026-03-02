import { Container, MainText, ShadowButton } from "@/components/widgets"
import { Constants } from "@/theme"
import { scopedI18n } from "@/translations/i18n"
import { View, Platform, Linking } from "react-native"

export default function Update () {

  const t = scopedI18n('error.update')

  function openStore () {
    const appStoreUrl = 'https://apps.apple.com/us/app/mygrid/id6739147623';
    const playStoreUrl = 'https://play.google.com/store/apps/details?id=com.theoduh.mygridapp';
  
    const storeUrl = Platform.OS === 'ios' ? appStoreUrl : playStoreUrl;
  
    Linking.openURL(storeUrl).catch((err) => console.error('Failed to open store:', err));
  };

  return (
    <Container style={{ backgroundColor: 'transparent' }}>
      <View style={{ width: '80%' }}>
        <MainText style={{ fontSize: Constants.fontSizes.title, marginBottom: 40 }}>{t('version')}</MainText>
        <MainText>{t('please')}</MainText>
        <ShadowButton style={{ marginTop: 40, height: 44, alignSelf: 'center', paddingHorizontal: 20 }} onPress={openStore}>
          <MainText>{t('update')}</MainText>
        </ShadowButton>
      </View>
    </Container>
  )
}