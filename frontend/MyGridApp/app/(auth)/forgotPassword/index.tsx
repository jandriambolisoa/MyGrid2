import { BackButton, Container, MainText, ShadowButton } from "@/components/widgets";
import { Constants, GlobalStyles, Colors } from "@/theme";
import { scopedI18n } from "@/translations/i18n";
import { useState } from "react";
import { Keyboard, KeyboardAvoidingView, TouchableWithoutFeedback, TextInput, ActivityIndicator } from "react-native";
import { useRouter } from "expo-router";
import { forgotPassword } from "@/api/forgotPassword";
import { useToast } from "@/contexts/ToastContext";

export default function ForgotPassword () {

  const t = scopedI18n('auth.forgotPassword');
  const router = useRouter();

  const { showToast } = useToast();

  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleForgot () {

    if (!email.length) {
      showToast({
        type: 'error',
        title: t('missingEmail')
      })
      return;
    }

    setLoading(true);

    const success = await forgotPassword(email)

    if (success) {
      router.push({
        pathname: '/forgotPassword/code',
        params: { email: email }
      });
      return;
    }

    router.push('/serverError');
  }

  return (
    <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
      <KeyboardAvoidingView style={{ flex: 1 }} behavior="padding">
        <Container style={{ backgroundColor: 'transparent' }}>
          <MainText fontSize='title' style={{ marginBottom: Constants.spacing.wideMargin }}>{t('forgotPassword')}</MainText>
          <MainText style={{ marginBottom: Constants.spacing.buttonMargin }}>{t('pleaseEnter')}</MainText>
          <TextInput
            value={email}
            placeholder={t('email')}
            keyboardType="email-address"
            cursorColor={Colors.light.lightText}
            selectionColor={Colors.light.lightText}
            style={[GlobalStyles.button, GlobalStyles.loginButton, { color: Colors.light.lightText, marginBottom: Constants.spacing.wideMargin }]}
            placeholderTextColor={Colors.light.disabledText}
            autoComplete='email'
            onChangeText={text => setEmail(text)}
          />
          <MainText style={{ marginBottom: Constants.spacing.buttonMargin, maxWidth: '80%' }}>{t('weWillSend')}</MainText>
          <ShadowButton style={[GlobalStyles.loginButton, { width: '50%', padding: 0 }]} onPress={handleForgot}>
            {loading ? <ActivityIndicator color={Colors.light.lightText}/> : <MainText>{t('sendEmail')}</MainText>}
          </ShadowButton>
          <BackButton marginTop={true}/>
        </Container>
      </KeyboardAvoidingView>
    </TouchableWithoutFeedback>
  )
}