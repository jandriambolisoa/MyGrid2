import { useState } from "react";
import { Container, LiteButton, MainText } from "@/components/widgets";
import { Dimensions, Keyboard, TextInput, TouchableWithoutFeedback, TouchableOpacity, View } from "react-native";
import { scopedI18n } from "@/translations/i18n";
import { GlobalStyles, Colors, Constants } from "@/theme";
import { Octicons } from '@expo/vector-icons';
import { useEmailLogin } from "@/hooks";

export default function Login () {

  const t = scopedI18n('auth.login');
  const width = Dimensions.get('window').width;

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPass, setShowPass] = useState(false);

  const { emailLogin, error, loading } = useEmailLogin();

  function handleLogin () {
    emailLogin(username, password);
  }

  return (
    <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
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
          <MainText>{t('login')}</MainText>
        </LiteButton>
      </Container>
    </TouchableWithoutFeedback>
  )
}