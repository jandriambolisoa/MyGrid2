import { Container, MainText, ShadowButton } from "@/components/widgets";
import { Constants, GlobalStyles, Colors } from "@/theme";
import { scopedI18n } from "@/translations/i18n";
import { useState, useEffect } from "react";
import { Keyboard, KeyboardAvoidingView, TouchableWithoutFeedback, TextInput, ActivityIndicator } from "react-native";
import { useEmailLogin } from "@/hooks";
import { useAuth } from "@/contexts/AuthContext";
import { useLocalSearchParams, useRouter } from "expo-router";
import { registerPushToken } from "@/api/registerPushToken";
import { getPushTokenAsync, checkVersion } from "@/utils";
import * as SecureStore from 'expo-secure-store';

export default function ForgotPassword () {

  const auth = useAuth();
  const t = scopedI18n('auth.forgotPassword')
  const router = useRouter();

  const { email } = useLocalSearchParams();
  const { loading, error, emailLogin } = useEmailLogin();

  const [code, setCode] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  useEffect(() => {
    if (error) {
      if (error === 'SERVER') {
        router.push('/serverError');
        return;
      }
      setErrorMsg(error);
    }
  }, [error])

  async function handleLogin () {

    setErrorMsg('');

    if (code.length !== 6) {
      setErrorMsg(t('missingInfo'));
      return;
    }

    const data = await emailLogin(email as string, code);

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
          <MainText fontSize='title' style={{ marginBottom: Constants.spacing.wideMargin }}>{t('forgotPassword')}</MainText>
          <MainText style={{ maxWidth: '80%', marginBottom: Constants.spacing.buttonMargin }}>{t('pleaseEnterCode')}</MainText>
          <TextInput
            value={code}
            keyboardType="number-pad"
            cursorColor={Colors.light.lightText}
            selectionColor={Colors.light.lightText}
            style={[GlobalStyles.button, GlobalStyles.loginButton, {
              color: Colors.light.lightText,
              marginBottom: Constants.spacing.wideMargin,
              width: '40%',
              textAlign: 'center',
              fontSize: Constants.fontSizes.header
            }]}
            placeholderTextColor={Colors.light.disabledText}
            onChangeText={text => setCode(text)}
            maxLength={6}
          />
          <ShadowButton style={[GlobalStyles.loginButton, { width: '50%', padding: 0 }]} onPress={handleLogin}>
            {loading ? <ActivityIndicator color={Colors.light.lightText}/> : <MainText>{t('confirm')}</MainText>}
          </ShadowButton>
          <MainText style={GlobalStyles.warning}>{errorMsg}</MainText>
        </Container>
      </KeyboardAvoidingView>
    </TouchableWithoutFeedback>
  )
}