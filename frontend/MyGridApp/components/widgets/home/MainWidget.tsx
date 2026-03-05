import { GlobalStyles, Constants, Colors } from "@/theme";
import { View, ViewProps, StyleSheet, Image, FlatList } from "react-native";
import { ShadowSetup, MainText, SpotLight, LiteButton, Sticker } from "@/components/widgets";
import { DateTime } from "luxon"
import { fromToDatetime, niceDatetime } from "@/utils"
import { scopedI18n } from "@/translations/i18n";
import { useRouter } from "expo-router";

export type MainWidgetProps = ViewProps & {
  datas?: any
}

export function MainWidget({ 
  datas = null,
  style,
  ...otherProps
}: MainWidgetProps) {

  const t = scopedI18n('widgets.mainWidget');
  const router = useRouter()

  const color1 = datas.event.colors[0];
  const color2 = datas.event.colors.length > 1 ? datas.event.colors[1] : color1;

  function renderItem({item} : any) {

    function handlePress () {
      if (item.is_over) {
        if (item.has_prono) {
          router.push(`/sessions/results/${item.id}`);
          return;
        }
        
        router.push(`/sessions/resultsAlone/${item.id}`);
        return;
      }

      // Live session later
      
      router.push({
        pathname: `/sessions/predictions/${item.id}` as any,
        params: { hasProno: item.has_prono, hasStarted: String(hasStarted), datetime: item.datetime }
      })
      return;
    }

    const hasStarted = DateTime.fromISO(item.datetime) < DateTime.now()

    function rightItem () {
      if (item.is_over) {
        return (
          <MainText>{t('showResults')}</MainText>
        )
      }

      if (hasStarted) {

        if (!item.competitive && DateTime.fromISO(item.datetime).plus({ hour: 1 }) < DateTime.now()) {
          return (
            <MainText>{t('finished')}</MainText>
          )
        }
        return (
          <MainText style={{ color: Colors.light.live }}>{t('onGoing')}</MainText>
        )
      }

      return (
        <MainText>{niceDatetime(item.datetime)}</MainText>
      )
    }

    return(
      <View style={{ overflow: 'hidden', marginBottom: Constants.spacing.buttonPadding }}>
        <LiteButton style={[GlobalStyles.mainWidgetButton, { overflow: 'visible' }]} onPress={handlePress} disabled={item.competitive? false : true}>
          <MainText>{item.name}</MainText>
          {item.has_prono && <Sticker style={{ left: '30%' }}/>}
          {rightItem()}
        </LiteButton>
      </View>
    )
  }

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
        <FlatList
          data={datas.sessions}
          renderItem={renderItem}
          // Should be tested on android: nestedScrollEnabled
          showsVerticalScrollIndicator={false}
          style={{ alignSelf: "stretch" }}
        />
      </View>
    </View>
  )
}

/* Components removed (need tracks and trophies png files from backend)
<Image resizeMode="stretch" style={{ position: 'absolute', width: 50, height: 50, top: 20, right: "5%" }} source={require('@/assets/images/demo/spa.png')}/>
<Image resizeMode="contain" style={{ height: "30%", marginVertical: 30 }} source={require('@/assets/images/demo/trophy_belgium.png')}/>
*/