import { MainText, SpotLight, SessionsList, BackButton } from "@/components/widgets";
import { useLocalSearchParams } from "expo-router";
import { useApi } from "@/hooks";
import { useEffect, useState } from "react";
import { useAuth } from "@/contexts/AuthContext";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { Image, View, StyleSheet } from "react-native";
import { Colors, Constants } from "@/theme";
import { DateTime } from "luxon";
import { fromToDatetime } from "@/utils";
import { scopedI18n } from "@/translations/i18n";
import * as Localization from "expo-localization";

export default function Events () {

  const t = scopedI18n('widgets.mainWidget')
  const local = useLocalSearchParams();
  const auth = useAuth();
  const insets = useSafeAreaInsets();

  const locale = Localization.getLocales()[0]?.languageCode || 'en'

  const { datas, error, loading, api: getEvent } = useApi(true);

  const [eventDatas, setEventDatas] = useState<any>(null);

  console.log(local.eventName)

  useEffect(() => {
    auth && getEvent({
      //endpoint: `/events/search?q=${local.eventName}`,
      endpoint: `/events/search?q=${local.eventName}&language=${locale}`,
      auth
    })
  }, [auth])

  useEffect(() => {
    if (datas?.length) {
      setEventDatas(datas[0]);
    }
  }, [datas])

  function eventDatetime () {
    const lastEvent = eventDatas?.sessions?.reduce((prev: any, current: any) => 
      DateTime.fromISO(current.datetime) > DateTime.fromISO(prev.datetime) ? current : prev
    );
    return fromToDatetime(lastEvent.datetime)
  }

  const color1 = eventDatas?.colors?.[0];
  const color2 = eventDatas?.colors?.[1] ?? color1;

  console.log(eventDatas)

  return (
    <View style={{ flex: 1, backgroundColor: Colors.light.background }}>
      {eventDatas &&
      <>
        <SpotLight color={color1} cx="35%" cy="35%" fx="5%" fy="5%" radius="50%"/>
        <SpotLight color={color2} cx="70%" cy="70%" fx="95%" fy="95%" radius="45%"/>
        <View style={[StyleSheet.absoluteFill, { padding: Constants.spacing.buttonPadding , alignItems: 'center', paddingTop: insets.top }]}>
          <MainText style={{ fontSize: Constants.fontSizes.title, marginTop: Constants.spacing.mainWidgetMargin }}>{eventDatas.name}</MainText>
          <Image source={{ uri: eventDatas.flag }} style={[{ width: 200, height: 50 }]} resizeMode="contain"/>
          <MainText style={{ marginBottom: 40, marginTop: Constants.spacing.mainWidgetMargin }}>{eventDatetime()}</MainText>
          <MainText style={{ alignSelf: 'flex-start', marginBottom: Constants.spacing.buttonPadding }}>{t('sessions')}</MainText>
          {eventDatas.sessions && <SessionsList datas={eventDatas.sessions}/>}
        </View>
      </>
      }
      <BackButton style={{ height: Constants.spacing.backButtonSize, top: insets.top }}/>
    </View>
  )
}