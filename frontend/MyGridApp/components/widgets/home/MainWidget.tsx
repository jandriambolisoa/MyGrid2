import { GlobalStyles, Constants } from "@/theme";
import { View, ViewProps, StyleSheet, Image } from "react-native";
import { ShadowSetup, MainText, SpotLight, SessionsList } from "@/components/widgets";
import { DateTime } from "luxon"
import { fromToDatetime } from "@/utils"
import { scopedI18n } from "@/translations/i18n";

export type MainWidgetProps = ViewProps & {
  datas?: any
}

export function MainWidget({ 
  datas = null,
  style,
  ...otherProps
}: MainWidgetProps) {

  const t = scopedI18n('widgets.mainWidget');

  const color1 = datas.event.colors[0];
  const color2 = datas.event.colors.length > 1 ? datas.event.colors[1] : color1;

  function eventDatetime () {
    const lastEvent = datas.sessions.reduce((prev: any, current: any) => 
      DateTime.fromISO(current.datetime) > DateTime.fromISO(prev.datetime) ? current : prev
    );
    return fromToDatetime(lastEvent.datetime)
  }

  return (
    <View style={[GlobalStyles.button, GlobalStyles.mainWidget, style]} {...otherProps}>
      <SpotLight color={color1} cx="35%" cy="35%" fx="5%" fy="5%" radius="50%"/>
      <SpotLight color={color2} cx="70%" cy="70%" fx="95%" fy="95%" radius="45%"/>
      <ShadowSetup />
      <View style={[StyleSheet.absoluteFill, { padding: Constants.spacing.buttonPadding , alignItems: 'center' }]}>
        <MainText style={{ fontSize: Constants.fontSizes.title, marginTop: Constants.spacing.mainWidgetMargin }}>{datas.event.name}</MainText>
        <Image source={{ uri: datas.event.flag }} style={{ width: 200, height: 50 }} resizeMode="contain"/>
        <MainText style={{ marginBottom: 40, marginTop: Constants.spacing.mainWidgetMargin }}>{eventDatetime()}</MainText>
        <MainText style={{ alignSelf: 'flex-start', marginBottom: Constants.spacing.buttonPadding }}>{t('sessions')}</MainText>
        <SessionsList datas={datas.sessions}/>
      </View>
    </View>
  )
}

/* Components removed (need tracks and trophies png files from backend)
<Image resizeMode="stretch" style={{ position: 'absolute', width: 50, height: 50, top: 20, right: "5%" }} source={require('@/assets/images/demo/spa.png')}/>
<Image resizeMode="contain" style={{ height: "30%", marginVertical: 30 }} source={require('@/assets/images/demo/trophy_belgium.png')}/>
*/