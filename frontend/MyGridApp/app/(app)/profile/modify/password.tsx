import { BackButton, Container, MainText, ShadowButton } from "@/components/widgets";
import { TextInput, TouchableWithoutFeedback, Keyboard, KeyboardAvoidingView, ActivityIndicator } from "react-native";
import { useState, useEffect } from "react";
import { Colors, GlobalStyles, Constants } from "@/theme";
import { scopedI18n } from "@/translations/i18n";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { useApi } from "@/hooks";
import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "expo-router";

export default function ModifyPassword () {

  const t = scopedI18n('profile.modify');
  const insets = useSafeAreaInsets();
  const auth = useAuth();
  const router = useRouter();

  const [oldP, setOldP] = useState('');
  const [newP, setNewP] = useState('');
  const [confirmP, setConfirmP] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  const { error, loading, api: modifyPassword } = useApi();

  useEffect(() => {
    if (error) {
      setErrorMsg(error);
    }
  }, [error])

  async function modify () {

    setErrorMsg('')

    if (oldP.length === 0 || newP.length === 0 || confirmP.length === 0) {
      setErrorMsg(t('missingInfo'));
      return;
    }

    if (newP !== confirmP) {
      setErrorMsg(t('passwordsDontMatch'));
      return;
    }

    const success = await modifyPassword({
      endpoint: '/users/profile/edit/password',
      body: {
        old_password: oldP,
        new_password: newP
      },
      method: 'PUT',
      auth: auth
    })

    if (success) {
      router.push('/profile/modify/passwordModified')
    }

  }

  return (
    <TouchableWithoutFeedback onPress={() => Keyboard.dismiss()}>
      <KeyboardAvoidingView style={{ flex: 1 }} behavior="padding">
        <Container style={{ backgroundColor: 'transparent' }}>
          <MainText fontSize="title" style={{ marginBottom: 44 }}>{t('modifyPassword')}</MainText>
          <TextInput
            value={oldP}
            placeholder={t('oldPassword')}
            cursorColor={Colors.light.lightText}
            selectionColor={Colors.light.lightText}
            style={[GlobalStyles.button, GlobalStyles.loginButton]}
            placeholderTextColor={Colors.light.disabledText}
            autoComplete='password'
            onChangeText={text => setOldP(text)}
            secureTextEntry={true}
          />
          <TextInput
            value={newP}
            placeholder={t('newPassword')}
            cursorColor={Colors.light.lightText}
            selectionColor={Colors.light.lightText}
            style={[GlobalStyles.button, GlobalStyles.loginButton]}
            placeholderTextColor={Colors.light.disabledText}
            onChangeText={text => setNewP(text)}
            secureTextEntry={true}
          />
          <TextInput
            value={confirmP}
            placeholder={t('confirmPassword')}
            cursorColor={Colors.light.lightText}
            selectionColor={Colors.light.lightText}
            style={[GlobalStyles.button, GlobalStyles.loginButton]}
            placeholderTextColor={Colors.light.disabledText}
            onChangeText={text => setConfirmP(text)}
            secureTextEntry={true}
          />
          <ShadowButton style={{ width: '45%' }} onPress={modify}>
            {loading ? <ActivityIndicator color={Colors.light.lightText}/> : <MainText>{t('modify')}</MainText>}
          </ShadowButton>
          <BackButton style={{ justifyContent: 'flex-start', paddingTop: insets.top + Constants.spacing.mainWidgetMargin, height: 60 + insets.top }}/>
          <MainText style={GlobalStyles.warning}>{errorMsg}</MainText>
        </Container>
      </KeyboardAvoidingView>
    </TouchableWithoutFeedback>
  )
}