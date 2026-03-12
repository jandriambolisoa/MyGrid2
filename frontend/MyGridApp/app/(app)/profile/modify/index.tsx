import { Container, Header, ProfilePicture, ShadowButton, MainText } from '@/components/widgets'
import { useAuth } from "@/contexts/AuthContext"
import { scopedI18n } from '@/translations/i18n'
import { useEffect, useState } from 'react'
import { View, Alert, ActivityIndicator } from 'react-native'
import * as ImagePicker from "expo-image-picker"
import { ImageManipulator, SaveFormat } from "expo-image-manipulator"
import { useApi } from '@/hooks'
import { Colors, Constants } from '@/theme'
import { useRouter } from 'expo-router'

export default function Modify () {

  const t = scopedI18n('profile.modify');
  const auth = useAuth();
  const router = useRouter();

  const { loading: imageLoading, api: postImage } = useApi();
  const { datas: userDatas, api: getUser } = useApi(false, false);

  const [headerHeight, setHeaderHeight] = useState(0);

  useEffect(() => {
    if (userDatas) {
      auth.storeUser(userDatas.user);
    }
  }, [userDatas, auth])

  const pickImage = async () => {
    const permissionResult = await ImagePicker.requestMediaLibraryPermissionsAsync();

    if (!permissionResult.granted) {
      Alert.alert(t('permission'), t('permissionTo'));
    }

    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ['images'],
      allowsEditing: true,
      aspect: [1, 1],
      quality: 1
    })

    if (!result.canceled) {

      const context = ImageManipulator.manipulate(result.assets[0].uri);
      context.resize({ width: 256, height: 256 });
      const image = await context.renderAsync();
      const resizedImage = await image.saveAsync({ compress: 1, format: SaveFormat.JPEG });

      const uri = resizedImage.uri;
      
      const uriParts = uri.split('/');
      const filename = uriParts[uriParts.length - 1];

      const formData = new FormData();
      formData.append('image', {
        uri: uri,
        name: filename,
        type: 'image/jpeg'
      } as any);
      
      await postImage({
        endpoint: '/users/profile/edit/pp',
        body: formData,
        method: 'PUT',
        contentType: 'multipart/form-data',
        auth: auth
      })

      await getUser({
        endpoint: '/users/profile',
        auth: auth
      })
    }
  }

  function ppButton () {
    if (imageLoading) {
      return <ActivityIndicator color={Colors.light.lightText}/>
    }
    return <MainText>{t('modifyPP')}</MainText>
  }

  return (
    <Container style={{ backgroundColor: 'transparent', justifyContent: 'flex-start', paddingTop: headerHeight }}>
      <Header title={t('modifyProfile')} onLayout={(e) => setHeaderHeight(e.nativeEvent.layout.height)}>
        <View style={{ height: 20 }}/>
      </Header>
      <ProfilePicture link={auth.user?.image_url} size={100} borders={true} style={{ marginVertical: 44 }}/>
      <View style={{ width: '80%'}}>
        <ShadowButton style={{ alignSelf: 'stretch', marginBottom: Constants.spacing.buttonMargin }} onPress={pickImage}>
          {ppButton()}
        </ShadowButton>
        <ShadowButton style={{ alignSelf: 'stretch' }} onPress={() => router.push('/profile/modify/password')}>
          <MainText>{t('modifyPassword')}</MainText>
        </ShadowButton>
      </View>
    </Container>
  )
}