import { TouchableOpacity, View, ViewStyle } from "react-native";
import { MainText, ProfilePicture, ShadowSetup, SpotLight } from "@/components/widgets";
import { Constants, GlobalStyles, Colors } from "@/theme";
import { useAuth } from "@/contexts/AuthContext";
import { scopedI18n } from "@/translations/i18n";

function PodiumButton ({
  item=null,
  style,
} : {
  item?: any;
  style?: ViewStyle;
}) {

  const t = scopedI18n('home.social')

  const { user } = useAuth()

  const you = user?.username === item?.user?.username ? true : false

  // Replacing color - tmp
  const color = you ? Colors.light.warning : "#03051F"

  return (
    <TouchableOpacity
    style={[GlobalStyles.button, { flex: 1, justifyContent: 'flex-start' }, style]}
    >
      <SpotLight color={color} cx="60%" cy="60%" fx="80%" fy="70%" radius="70%" opacityStart="0.8" opacityEnd="0.1"/>
      <ShadowSetup/>
      <View style={{ justifyContent: 'space-between', flex: 1, padding: Constants.spacing.buttonPadding }}>
        <View>
          <MainText fontSize='title' bold={true}>{item.rank}</MainText>
          <ProfilePicture link={item.user.image_url} style={{ alignSelf: 'center', marginVertical: Constants.spacing.listMargin }}/>
          <MainText fontSize="small">{item.user.username}</MainText>
        </View>
        <View>
          <MainText fontSize='small'>{item.event.name}</MainText>
          <MainText fontSize='small'>{item.session.name}</MainText>
        </View>
        <MainText bold={true}>{item.score} {t('pts')}</MainText>
      </View>
    </TouchableOpacity>
  )
}

export function RecordsWidget ({
  type='sessions',
  datas=null
} : {
  type?: 'sessions' | 'events';
  datas: any;
}) {

  const t = scopedI18n('home.social')

  return (
    <View style={[GlobalStyles.button, { height: 320 }]}>
      {<SpotLight cx='50%' cy='10%' fx='40%' fy='10%' color={Colors.light.records}/>}
      <MainText bold={true} fontSize='header' style={{ marginTop: Constants.spacing.buttonPadding }}>{type === 'sessions' ? t('sessionRecords') : t('eventRecords')}</MainText>
      <View style={{ flexDirection: 'row', flex: 1, alignItems: 'flex-end', margin: Constants.spacing.listMargin, marginTop: Constants.spacing.mainWidgetMargin }}>
        <PodiumButton style={{ height: '90%', marginEnd: Constants.spacing.listMargin }} item={datas?.[1]}/>
        <PodiumButton style={{ height: '100%', marginEnd: Constants.spacing.listMargin }} item={datas?.[0]}/>
        <PodiumButton style={{ height: '80%' }} item={datas?.[2]}/>
      </View>
    </View>
  )
}