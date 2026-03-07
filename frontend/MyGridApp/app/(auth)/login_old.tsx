import { Container, SpotLight, MainText } from "@/components/widgets";
import { TouchableOpacity, View } from "react-native";
import { AntDesign } from "@expo/vector-icons";
import { scopedI18n } from "@/translations/i18n";
import * as AppleAuthentication from 'expo-apple-authentication';
import * as Google from 'expo-auth-session/providers/google';
import * as WebBrowser from 'expo-web-browser';
import { useEffect } from "react";

const t = scopedI18n('auth.login')

WebBrowser.maybeCompleteAuthSession();

export default function Login () {

  const [request, response, promptAsync] = Google.useIdTokenAuthRequest({
    webClientId: "506627688155-vnssthto3rl9d12ts93o9nsnc0bhdobs.apps.googleusercontent.com",
    iosClientId: "506627688155-gk31l5ohis7ded2596lm5447mcrc5apl.apps.googleusercontent.com",
    scopes: ['openid', 'profile', 'email']
  })

  /*const [request, response, promptAsync] = Google.useAuthRequest({
    webClientId: "506627688155-vnssthto3rl9d12ts93o9nsnc0bhdobs.apps.googleusercontent.com",
    iosClientId: "506627688155-gk31l5ohis7ded2596lm5447mcrc5apl.apps.googleusercontent.com",
    scopes: ['profile', 'email']
  })*/

  useEffect(() => {
    if (response?.type === 'success') {
      //const { authentication } = response;
      console.log("Auth:", response.params.id_token);
    }
  }, [response])

  async function handleGoogle () {
    await promptAsync()
  }

  async function handleApple () {
    try {
      const credential = await AppleAuthentication.signInAsync({
        requestedScopes: [
          AppleAuthentication.AppleAuthenticationScope.FULL_NAME,
          AppleAuthentication.AppleAuthenticationScope.EMAIL,
        ],
      });
      
      if (credential) {
        console.log(credential)
      }
    } catch (e: any) {
      if (e.code === 'ERR_REQUEST_CANCELED') {
        // handle that the user canceled the sign-in flow
      } else {
        // handle other errors
      }
    }
  }

  return (
    <View style={{flex: 1}}>
      <SpotLight color="#00FFEE" cx="75%" cy="25%" fx="80%" fy="20%"/>
      <SpotLight color="#FF9900" cx="25%" cy="75%" fx="20%" fy="80%"/>
      <Container style={{ justifyContent: 'center', alignItems: 'center', backgroundColor: '#dddddd'}}>
        <TouchableOpacity onPress={handleGoogle} style={{borderWidth: 1, borderColor: 'white', padding: 10, borderRadius: 4, flexDirection: 'row'}}>
          <MainText>{t('signInGoogle')}</MainText>
          <AntDesign name="google" size={18} color="white" style={{ marginLeft: 8 }} />
        </TouchableOpacity>
        <TouchableOpacity onPress={handleApple} style={{borderWidth: 1, borderColor: 'white', padding: 10, borderRadius: 4, marginTop: 18, flexDirection: 'row'}}>
          <MainText>{t('signInApple')}</MainText>
          <AntDesign name="apple" size={18} color="white" style={{ marginLeft: 8}} />
        </TouchableOpacity>
      </Container>
    </View>
  )
}