import { useEffect, useState } from "react";
import { Container, ShadowButton, MainText } from "@/components/widgets";
import { Dimensions, Keyboard, TextInput, TouchableWithoutFeedback, TouchableOpacity, View, ActivityIndicator, KeyboardAvoidingView } from "react-native";
import { scopedI18n } from "@/translations/i18n";
import { GlobalStyles, Colors, Constants } from "@/theme";
import { Octicons } from '@expo/vector-icons';
import { useEmailLogin } from "@/hooks";
import { useRouter } from "expo-router";
import { useAuth } from "@/contexts/AuthContext";
import { checkVersion, getPushTokenAsync } from "@/utils";
import * as SecureStore from "expo-secure-store";
import { registerPushToken } from "@/api/registerPushToken";

export default function Login () {

  const t = scopedI18n('auth.login');
  const width = Dimensions.get('window').width;
  const router = useRouter();

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPass, setShowPass] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  const { emailLogin, error, loading } = useEmailLogin();
  const auth = useAuth();

  useEffect(() => {
    if (error) {
      setErrorMsg(error);
    }
  }, [error])

  async function handleLogin () {

    setErrorMsg('');

    if (username.length === 0 || password.length === 0) {
      setErrorMsg(t('missingInfo'));
      return;
    }

    const data = await emailLogin(username, password);

    if (data) {

      const loginDatas = {
        user: data.user,
        accessToken: data.access_token.access_token,
        refreshToken: data.refresh_token.refresh_token
      };

      await auth.login(loginDatas);

      if (data.app_status.maintenance) {
        router.replace('/error/maintenance');
        return;
      }

      if (!checkVersion(data.app_status.version)) {
        router.replace('/error/update');
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
  }

  return (
    <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
      <KeyboardAvoidingView style={{ flex: 1 }} behavior="padding">
        <Container style={{ backgroundColor: 'transparent' }}>
          <MainText style={{fontSize: Constants.fontSizes.big, marginBottom: 40}}>{t('login')}</MainText>
          <TextInput
            value={username}
            placeholder={t('usernameEmail')}
            keyboardType="email-address"
            cursorColor={Colors.light.lightText}
            selectionColor={Colors.light.lightText}
            style={[GlobalStyles.button, GlobalStyles.loginButton, { width: width * 0.7, color: Colors.light.lightText, marginBottom: Constants.spacing.buttonMargin }]}
            placeholderTextColor={Colors.light.disabledText}
            autoComplete='username'
            onChangeText={text => setUsername(text)}
          />
          <View style={{ alignSelf: 'stretch' }}>
            <TextInput
              value={password}
              placeholder={t('password')}
              placeholderTextColor={Colors.light.disabledText}
              cursorColor={Colors.light.lightText}
              selectionColor={Colors.light.lightText}
              style={[GlobalStyles.button, GlobalStyles.loginButton]}
              secureTextEntry={showPass ? false : true}
              autoComplete='password'
              onChangeText={text => setPassword(text)}
            />
            {password.length > 0 && <TouchableOpacity style={GlobalStyles.eye} onPress={() => setShowPass(!showPass)}>
              <Octicons name={showPass ? 'eye-closed' : 'eye'} size={20} color={Colors.light.lightText}/>
            </TouchableOpacity>}
          </View>
          <ShadowButton style={[GlobalStyles.loginButton, { width: width * 0.5, padding: 0 }]} onPress={handleLogin}>
            {loading ? <ActivityIndicator color={Colors.light.lightText}/> : <MainText>{t('login')}</MainText>}
          </ShadowButton>
          <TouchableOpacity style={GlobalStyles.authLink} onPress={() => router.replace('/signup')} hitSlop={10}>
            <MainText>{t('signup')}</MainText>
          </TouchableOpacity>
          <MainText style={GlobalStyles.warning}>{errorMsg}</MainText>
        </Container>
      </KeyboardAvoidingView>
    </TouchableWithoutFeedback>
  )
}