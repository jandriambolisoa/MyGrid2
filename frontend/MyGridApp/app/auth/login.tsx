import { useEffect, useState } from "react";
import { Container, LiteButton, MainText } from "@/components/widgets";
import { Dimensions, Keyboard, TextInput, TouchableWithoutFeedback, TouchableOpacity, View, ActivityIndicator, KeyboardAvoidingView } from "react-native";
import { scopedI18n } from "@/translations/i18n";
import { GlobalStyles, Colors, Constants } from "@/theme";
import { Octicons } from '@expo/vector-icons';
import { useEmailLogin } from "@/hooks";
import * as Localization from 'expo-localization';
import { useRouter } from "expo-router";
import { useAuth } from "@/contexts/AuthContext";

export default function Login () {

  const t = scopedI18n('auth.login');
  const width = Dimensions.get('window').width;
  const locale = Localization.getLocales()[0]?.languageCode || 'en';
  const router = useRouter();

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPass, setShowPass] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  const { emailLogin, error, loading } = useEmailLogin();
  const { login } = useAuth();

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

    const data = await emailLogin(username, password, locale);

    if (data) {
      await login(data);

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
          <View>
          <TextInput
            value={password}
            placeholder={t('password')}
            placeholderTextColor={Colors.light.disabledText}
            cursorColor={Colors.light.lightText}
            selectionColor={Colors.light.lightText}
            style={[GlobalStyles.button, GlobalStyles.loginButton, { width: width * 0.7, color: Colors.light.lightText }]}
            secureTextEntry={showPass ? false : true}
            autoComplete='password'
            onChangeText={text => setPassword(text)}
          />
          {password.length > 0 && <TouchableOpacity style={GlobalStyles.eye} onPress={() => setShowPass(!showPass)}>
            <Octicons name={showPass ? 'eye-closed' : 'eye'} size={20} color={Colors.light.lightText}/>
          </TouchableOpacity>}
          </View>
          <LiteButton style={[GlobalStyles.loginButton, { width: width * 0.5, marginTop: Constants.spacing.buttonMargin  }]} onPress={handleLogin}>
            {loading ? <ActivityIndicator color={Colors.light.lightText}/> : <MainText>{t('login')}</MainText>}
          </LiteButton>
          <MainText style={{ position: 'absolute', bottom: '20%', color: Colors.light.warning }}>{errorMsg}</MainText>
        </Container>
      </KeyboardAvoidingView>
    </TouchableWithoutFeedback>
  )
}