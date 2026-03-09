import { useEffect, useState } from "react";
import { Container, ShadowButton, MainText, PasswordInput } from "@/components/widgets";
import { Dimensions, Keyboard, TextInput, TouchableWithoutFeedback, TouchableOpacity, View, ActivityIndicator, KeyboardAvoidingView, Linking } from "react-native";
import { scopedI18n } from "@/translations/i18n";
import { GlobalStyles, Colors, Constants } from "@/theme";
import { Octicons } from '@expo/vector-icons';
import { useEmailSignup } from "@/hooks";
import * as Localization from 'expo-localization';
import { useRouter } from "expo-router";
import { useAuth } from "@/contexts/AuthContext";

export default function Signup () {

  const t = scopedI18n('auth.signup');
  const width = Dimensions.get('window').width;
  const router = useRouter();
  const locale = Localization.getLocales()[0]?.languageCode || 'en';
  const link = locale === 'en' ? 'https://mygrid-app.com/app-privacy-policy' : 'https://mygrid-app.com/fr/app-privacy-policy'


  const [isChecked, setIsChecked] = useState(false)
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPass, setShowPass] = useState(false);
  const [showConfirmPass, setShowConfirmPass] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [keyboardVisible, setKeyboardVisible] = useState(false);

  const { emailSignup, error, loading } = useEmailSignup();
  const { login } = useAuth();

  useEffect(() => {
    const showSubscription = Keyboard.addListener('keyboardDidShow', () => setKeyboardVisible(true));
    const hideSubscription = Keyboard.addListener('keyboardDidHide', () => setKeyboardVisible(false));

    return () => {
      showSubscription.remove();
      hideSubscription.remove();
    };
  }, []);

  useEffect(() => {
    if (error) {
      setErrorMsg(error);
    }
  }, [error])

  async function handleSignup () {

    setErrorMsg('');

    if (username.length === 0 || email.length === 0 || password.length === 0 || confirmPassword.length === 0) {
      setErrorMsg(t('missingInfo'));
      return;
    }

    if (password !== confirmPassword) {
      setErrorMsg(t('passwordsDontMatch'));
      return;
    }

    if (!isChecked) {
      setErrorMsg(t('youMust'));
      return;
    }

    const data = await emailSignup(username, email, password, locale);

    if (data) {

      const loginDatas = {
        user: data.user,
        accessToken: data.access_token.access_token,
        refreshToken: data.refresh_token.refresh_token
      }

      await login(loginDatas);

      router.replace({
        pathname: '/verify',
        params: {
          maintenance: data.app_status.maintenance,
          version: data.app_status.version
        }
      })
    }
  }

  return (
    <TouchableWithoutFeedback onPress={() => {Keyboard.dismiss(); setKeyboardVisible(false)}}>
      <KeyboardAvoidingView style={{ flex: 1 }} behavior="padding">
        <Container style={{ backgroundColor: 'transparent' }}>
          {!keyboardVisible && <MainText style={{fontSize: Constants.fontSizes.big, marginBottom: 40}}>{t('signup')}</MainText>}
          <TextInput
            value={username}
            placeholder={t('username')}
            cursorColor={Colors.light.lightText}
            selectionColor={Colors.light.lightText}
            style={[GlobalStyles.button, GlobalStyles.loginButton]}
            placeholderTextColor={Colors.light.disabledText}
            autoComplete='username'
            onChangeText={text => setUsername(text)}
          />
          <TextInput
            value={email}
            keyboardType="email-address"
            placeholder={t('email')}
            cursorColor={Colors.light.lightText}
            selectionColor={Colors.light.lightText}
            style={[GlobalStyles.button, GlobalStyles.loginButton ]}
            placeholderTextColor={Colors.light.disabledText}
            autoComplete='email'
            onChangeText={text => setEmail(text)}
          />
          <PasswordInput
            password={password}
            showPass={showPass}
            setShowPass={() => setShowPass(!showPass)}
            placeholder={t('password')}
            onChangeText={text => setPassword(text)}
            autoComplete="new-password"
          />
          <PasswordInput
            password={confirmPassword}
            showPass={showConfirmPass}
            setShowPass={() => setShowConfirmPass(!showConfirmPass)}
            placeholder={t('confirmPassword')}
            onChangeText={text => setConfirmPassword(text)}
            autoComplete="new-password"
          />
          <View style={{ flexDirection: 'row', maxWidth: '90%', marginBottom: 20, alignItems: 'center' }}>
            <TouchableOpacity
              style={{
                width: 12,
                height: 12,
                borderColor: Colors.light.borders,
                borderWidth: 1,
                backgroundColor: isChecked ? Colors.light.borders : 'transparent',
                borderRadius: 4
              }}
              hitSlop={20}
              onPress={() => {if (isChecked) {setIsChecked(false)}else{setIsChecked(true)}}}
            />
            <MainText style={{ marginHorizontal: 6 }}>{t('iAccept')}</MainText>
            <TouchableOpacity onPress={() => Linking.openURL(link)}>
              <MainText style={{ color: Colors.light.link }}>{t('privacyPolicy')}</MainText>
            </TouchableOpacity>
          </View>
          <ShadowButton style={[GlobalStyles.loginButton, { width: width * 0.5, padding: 0 }]} onPress={handleSignup}>
            {loading ? <ActivityIndicator color={Colors.light.lightText}/> : <MainText>{t('signup')}</MainText>}
          </ShadowButton>
          {!keyboardVisible && <TouchableOpacity style={GlobalStyles.authLink} onPress={() => router.replace('/login')}>
            <MainText>{t('login')}</MainText>
          </TouchableOpacity>}
          <MainText style={GlobalStyles.warning}>{errorMsg}</MainText>
        </Container>
      </KeyboardAvoidingView>
    </TouchableWithoutFeedback>
  )
}