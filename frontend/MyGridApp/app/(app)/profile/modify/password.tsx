import { BackButton, Container, MainText, PasswordInput, ShadowButton } from "@/components/widgets";
import { TouchableWithoutFeedback, Keyboard, KeyboardAvoidingView, ActivityIndicator } from "react-native";
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
  const [showOldP, setShowOldP] = useState(false);
  const [showNewP, setShowNewP] = useState(false);
  const [showConfirmP, setShowConfirmP] = useState(false);

  const { error, loading, api: modifyPassword } = useApi(false, false);

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
          <PasswordInput 
            password={oldP}
            showPass={showOldP}
            setShowPass={() => setShowOldP(!showOldP)}
            placeholder={t('oldPassword')}
            onChangeText={text => setOldP(text)}
            autoComplete="current-password"
          />
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
          <BackButton style={{ justifyContent: 'flex-start', paddingTop: insets.top + Constants.spacing.mainWidgetMargin, height: 60 + insets.top }}/>
          <MainText style={GlobalStyles.warning}>{errorMsg}</MainText>
        </Container>
      </KeyboardAvoidingView>
    </TouchableWithoutFeedback>
  )
}