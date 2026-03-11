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
  const { id } = useLocalSearchParams();
  const auth = useAuth();
  const insets = useSafeAreaInsets();

  const locale = Localization.getLocales()[0]?.languageCode || 'en'

  const { datas, error, loading, api: getEvent } = useApi(true);

  useEffect(() => {
    auth && getEvent({
      endpoint: `/nav/home/events/${id}`,
      auth
    })
  }, [auth])

  function eventDatetime () {
    const lastEvent = datas.sessions?.reduce((prev: any, current: any) => 
      DateTime.fromISO(current.datetime) > DateTime.fromISO(prev.datetime) ? current : prev
    );
    return fromToDatetime(lastEvent.datetime)
  }

  const color1 = datas?.event?.colors?.[0];
  const color2 = datas?.event?.colors?.[1] ?? color1;

  return (
    <View style={{ flex: 1, backgroundColor: Colors.light.background }}>
      {datas &&
      <>
        <SpotLight color={color1} cx="35%" cy="35%" fx="5%" fy="5%" radius="50%"/>
        <SpotLight color={color2} cx="70%" cy="70%" fx="95%" fy="95%" radius="45%"/>
        <View style={[StyleSheet.absoluteFill, { padding: Constants.spacing.buttonPadding , alignItems: 'center', paddingTop: insets.top }]}>
          <MainText style={{ fontSize: Constants.fontSizes.title, marginTop: Constants.spacing.mainWidgetMargin }}>{datas.event?.name}</MainText>
          <Image source={{ uri: datas.event?.flag }} style={[{ width: 200, height: 50 }]} resizeMode="contain"/>
          <MainText style={{ marginBottom: 40, marginTop: Constants.spacing.mainWidgetMargin }}>{eventDatetime()}</MainText>
          <MainText style={{ alignSelf: 'flex-start', marginBottom: Constants.spacing.buttonPadding }}>{t('sessions')}</MainText>
          {datas.sessions && <SessionsList datas={datas.sessions}/>}
        </View>
      </>
      }
      <BackButton style={{ height: Constants.spacing.backButtonSize, top: insets.top }}/>
    </View>
  )
}