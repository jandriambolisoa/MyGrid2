import { View } from 'react-native';
import { useRouter } from 'expo-router';
import { Container, MainText, LiteButton } from '@/components/widgets';
import { Constants } from '@/theme';
import { useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import * as SecureStore from 'expo-secure-store';
import { refreshLogin } from '@/api/auth';

export default function MainScreen () {

  const router = useRouter();
  const { login, logout } = useAuth();

  useEffect(() => {
    async function initAuth () {

      const oldAccessToken = await SecureStore.getItemAsync('accessToken');
      const oldRefreshToken = await SecureStore.getItemAsync('refreshToken');

      try {
        const data = await refreshLogin(oldAccessToken, oldRefreshToken);

        const loginDatas = {
          user: data.user,
          accessToken: data.access_token.access_token,
          refreshToken: oldRefreshToken
        }

        console.log(loginDatas)

        await login(loginDatas)
        router.replace('/home')
      } catch (e) {
        console.log(e)
        logout();
        router.replace('/login')
      }
    }

    initAuth()
  })

  return (
    <Container style={{ backgroundColor: 'transparent'}}>
      
      <View style={{alignItems: 'center', justifyContent: 'center', position: 'absolute', top: "45%"}}>
        <MainText>Welcome to</MainText>
        <MainText style={{fontSize: Constants.fontSizes.giant, marginBottom: 40}}>Mygrid</MainText>
      </View>
      <LiteButton onPress={() => router.push('/login')} style={[{position: 'absolute', bottom: "30%"}]}>
        <MainText>Sign in</MainText>
      </LiteButton>
    </Container>
  )
}