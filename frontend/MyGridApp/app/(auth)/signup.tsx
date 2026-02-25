import { useEffect, useState } from "react";
import { Container, LiteButton, MainText } from "@/components/widgets";
import { Dimensions, Keyboard, TextInput, TouchableWithoutFeedback, TouchableOpacity, View, ActivityIndicator, KeyboardAvoidingView } from "react-native";
import { scopedI18n } from "@/translations/i18n";
import { GlobalStyles, Colors, Constants } from "@/theme";
import { Octicons } from '@expo/vector-icons';
import { useEmailSignup } from "@/hooks";
import * as Localization from 'expo-localization';
import { useRouter } from "expo-router";
import { useAuth } from "@/contexts/AuthContext";

// Should be removed later after backend udpate to log from signup request.
import { useEmailLogin } from "@/hooks";

export default function Signup () {

  const t = scopedI18n('auth.signup');
  const width = Dimensions.get('window').width;
  const locale = Localization.getLocales()[0]?.languageCode || 'en';
  const router = useRouter();

  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPass, setShowPass] = useState(false);
  const [showConfirmPass, setShowConfirmPass] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  const { emailSignup, error, loading } = useEmailSignup();
  const { emailLogin } = useEmailLogin();
  const { login } = useAuth();

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

    const data = await emailSignup(username, email, password, locale);

    if (data) {
      // Should be removed later after backend udpate to log from signup request.
      const loginData = await emailLogin(username, password, locale);

      if (loginData) {
        await login(loginData);

        router.replace('/home')
      }
    }
  }

  return (
    <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
      <KeyboardAvoidingView style={{ flex: 1 }} behavior="padding">
        <Container style={{ backgroundColor: 'transparent' }}>
          <MainText style={{fontSize: Constants.fontSizes.big, marginBottom: 40}}>{t('signup')}</MainText>
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
            placeholder={t('email')}
            cursorColor={Colors.light.lightText}
            selectionColor={Colors.light.lightText}
            style={[GlobalStyles.button, GlobalStyles.loginButton ]}
            placeholderTextColor={Colors.light.disabledText}
            autoComplete='email'
            onChangeText={text => setEmail(text)}
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
          <View style={{ alignSelf: 'stretch' }}>
            <TextInput
              value={confirmPassword}
              placeholder={t('confirmPassword')}
              placeholderTextColor={Colors.light.disabledText}
              cursorColor={Colors.light.lightText}
              selectionColor={Colors.light.lightText}
              style={[GlobalStyles.button, GlobalStyles.loginButton]}
              secureTextEntry={showConfirmPass ? false : true}
              autoComplete='password'
              onChangeText={text => setConfirmPassword(text)}
            />
            {confirmPassword.length > 0 && <TouchableOpacity style={GlobalStyles.eye} onPress={() => setShowConfirmPass(!showConfirmPass)}>
              <Octicons name={showConfirmPass ? 'eye-closed' : 'eye'} size={20} color={Colors.light.lightText}/>
            </TouchableOpacity>}
          </View>
          <LiteButton style={[GlobalStyles.loginButton, { width: width * 0.5 }]} onPress={handleSignup}>
            {loading ? <ActivityIndicator color={Colors.light.lightText}/> : <MainText>{t('signup')}</MainText>}
          </LiteButton>
          <TouchableOpacity style={GlobalStyles.authLink} onPress={() => router.replace('/login')}>
            <MainText>{t('login')}</MainText>
          </TouchableOpacity>
          <MainText style={GlobalStyles.warning}>{errorMsg}</MainText>
        </Container>
      </KeyboardAvoidingView>
    </TouchableWithoutFeedback>
  )
}