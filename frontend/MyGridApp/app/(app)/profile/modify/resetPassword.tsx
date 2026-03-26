import { Container, MainText, PasswordInput, ShadowButton } from "@/components/widgets";
import { TouchableWithoutFeedback, Keyboard, KeyboardAvoidingView, ActivityIndicator } from "react-native";
import { useState, useEffect } from "react";
import { Colors, GlobalStyles } from "@/theme";
import { scopedI18n } from "@/translations/i18n";
import { useApi } from "@/hooks";
import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "expo-router";

export default function ModifyPassword () {

  const t = scopedI18n('profile.modify');
  const auth = useAuth();
  const router = useRouter();

  const [newP, setNewP] = useState('');
  const [confirmP, setConfirmP] = useState('');
  const [errorMsg, setErrorMsg] = useState('');
  const [showNewP, setShowNewP] = useState(false);
  const [showConfirmP, setShowConfirmP] = useState(false);

  const { error, loading, api: resetPassword } = useApi(false, false);

  useEffect(() => {
    if (error) {
      setErrorMsg(error);
    }
  }, [error])

  async function modify () {

    setErrorMsg('')

    if (newP.length === 0 || confirmP.length === 0) {
      setErrorMsg(t('missingInfo'));
      return;
    }

    if (newP !== confirmP) {
      setErrorMsg(t('passwordsDontMatch'));
      return;
    }

    const success = await resetPassword({
      endpoint: '/users/profile/edit/reset-password',
      body: {
        old_password: "",
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
          <PasswordInput 
            password={newP}
            showPass={showNewP}
            setShowPass={() => setShowNewP(!showNewP)}
            placeholder={t('newPassword')}
            onChangeText={text => setNewP(text)}
            autoComplete="new-password"
          />
          <PasswordInput 
            password={confirmP}
            showPass={showConfirmP}
            setShowPass={() => setShowConfirmP(!showConfirmP)}
            placeholder={t('confirmPassword')}
            onChangeText={text => setConfirmP(text)}
            autoComplete="new-password"
          />
          <ShadowButton style={{ width: '45%' }} onPress={modify}>
            {loading ? <ActivityIndicator color={Colors.light.lightText}/> : <MainText>{t('modify')}</MainText>}
          </ShadowButton>
          <MainText style={GlobalStyles.warning}>{errorMsg}</MainText>
        </Container>
      </KeyboardAvoidingView>
    </TouchableWithoutFeedback>
  )
}