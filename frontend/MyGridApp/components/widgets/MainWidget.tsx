import { GlobalStyles, Constants, Colors } from "@/theme";
import { View, ViewProps, StyleSheet, Image, FlatList } from "react-native";
import { ShadowSetup, MainText, SpotLight, LiteButton } from "@/components/widgets";
import { DateTime } from "luxon"
import { niceDatetime } from "@/utils"
import { scopedI18n } from "@/translations/i18n";

export type MainWidgetProps = ViewProps & {
  datas?: any
}

export function MainWidget({ 
  datas = null,
  style,
  ...otherProps
}: MainWidgetProps) {

  // Temporary date to test with example datas
  const dateTemp = "2026-01-25T03:41:44.092651+01:00";

  const t = scopedI18n('widgets.mainWidget');

  const color1 = datas.event.colors[0];
  const color2 = datas.event.colors.length > 1 ? datas.event.colors[1] : color1;

  function renderItem({item} : any) {

    const disabledColor = item.is_over ? { color: Colors.light.disabled, borderColor: Colors.light.disabled } : { }

    function rightItem () {
      if (item.is_over) {
        return (
          <MainText style={{  }}>{t('showResults')}</MainText>
        )
      }

      if (DateTime.fromISO(item.datetime) < DateTime.fromISO(dateTemp)) {
        return (
          <MainText style={{ color: Colors.light.live }}>{t('live')}</MainText>
        )
      }

      return (
        <MainText>{niceDatetime(item.datetime)}</MainText>
      )
    }

    return(
      <LiteButton style={[disabledColor, { alignSelf: "stretch", flexDirection: "row", justifyContent: "space-between", marginBottom: Constants.spacing.buttonPadding }]}>
        <MainText style={[disabledColor]}>{item.name}</MainText>
        {rightItem()}
      </LiteButton>
    )
  }

  return (
    <View style={[GlobalStyles.button, GlobalStyles.mainWidget, style]} {...otherProps}>
      <SpotLight color={color1} cx="35%" cy="35%" fx="5%" fy="5%" radius="50%"/>
      <SpotLight color={color2} cx="70%" cy="70%" fx="95%" fy="95%" radius="45%"/>
      <ShadowSetup />
      <View style={[StyleSheet.absoluteFill, { padding: Constants.spacing.buttonPadding , alignItems: 'center' }]}>
        <MainText style={{ fontSize: 28, marginTop: 20 }}>{datas.event.name}</MainText>
        <Image resizeMode="stretch" style={{ position: 'absolute', width: 50, height: 50, top: 20, right: "10%" }} source={require('@/assets/images/demo/spa.png')}/>
        <Image resizeMode="contain" style={{ height: "30%", marginVertical: 30 }} source={require('@/assets/images/demo/trophy_belgium.png')}/>
        <FlatList
          data={datas.sessions}
          renderItem={renderItem}
          scrollEnabled={false}
          style={{ alignSelf: "stretch" }}
        />
      </View>
    </View>
  )
}