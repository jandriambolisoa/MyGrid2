import { View } from 'react-native';
import { useRouter } from 'expo-router';
import { Container, MainText } from '@/components/widgets';
import { Constants } from '@/theme';
import { useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import * as SecureStore from 'expo-secure-store';
import { refreshLogin } from '@/api/refresh';
import { checkVersion, getPushTokenAsync } from '@/utils';
import { scopedI18n } from '@/translations/i18n';
import { registerPushToken } from '@/api/registerPushToken';

export default function MainScreen () {

  const router = useRouter();
  const t = scopedI18n('index')

  const { login, logout } = useAuth();

  useEffect(() => {
    async function initAuth () {

      const oldAccessToken = await SecureStore.getItemAsync('accessToken');
      const oldRefreshToken = await SecureStore.getItemAsync('refreshToken');

      if (!oldRefreshToken) {
        logout();
        router.replace('/login')
        return
      }

      let data;

      try {
        data = await refreshLogin(oldAccessToken, oldRefreshToken);
      } catch (e: any) {

        if (e.message === 'AUTH') {
          logout();
          router.replace('/login');
          return;
        }

        router.replace('/serverError');
        return;
      }

      const loginDatas = {
        user: data.user,
        accessToken: data.access_token.access_token,
        refreshToken: oldRefreshToken
      }

      await login(loginDatas)

      if (data.app_status.maintenance) {
        router.replace('/error/maintenance')
        return;
      }

      if (!checkVersion(data.app_status.version)) {
        router.replace('/error/update')
        return;
      }

      const pushToken = await getPushTokenAsync();
      const oldPushToken = await SecureStore.getItemAsync('pushToken');

      try {
        if (pushToken && pushToken !== oldPushToken) {
          await registerPushToken(data.access_token.access_token, pushToken)
        }
      } catch (e) {
        console.log(e)
      }

      router.replace('/home')
    }

    initAuth()
  }, [])

  return (
    <Container style={{ backgroundColor: 'transparent'}}>
      <View style={{alignItems: 'center', justifyContent: 'center', position: 'absolute', top: "45%"}}>
        <MainText>{t('welcome')}</MainText>
        <MainText style={{fontSize: Constants.fontSizes.giant, marginBottom: 40}}>{t('mygrid')}</MainText>
      </View>
    </Container>
  )
}