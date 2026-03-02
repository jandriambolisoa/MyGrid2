import { View } from 'react-native';
import { useRouter } from 'expo-router';
import { Container, MainText, LiteButton } from '@/components/widgets';
import { Constants } from '@/theme';
import { useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import * as SecureStore from 'expo-secure-store';
import { refreshLogin } from '@/api/refresh';
import { checkVersion } from '@/utils';

export default function MainScreen () {

  const router = useRouter();
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

      try {
        const data = await refreshLogin(oldAccessToken, oldRefreshToken);

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

        router.replace('/home')

      } catch (e) {
        logout();
        router.replace('/login')
      }
    }

    initAuth()
  }, [])

  return (
    <Container style={{ backgroundColor: 'transparent'}}>
      <View style={{alignItems: 'center', justifyContent: 'center', position: 'absolute', top: "45%"}}>
        <MainText>Welcome to</MainText>
        <MainText style={{fontSize: Constants.fontSizes.giant, marginBottom: 40}}>Mygrid</MainText>
      </View>
    </Container>
  )
}