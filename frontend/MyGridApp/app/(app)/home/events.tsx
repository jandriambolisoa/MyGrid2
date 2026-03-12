import { ScrollContainer, MainWidget, ChampionshipWidget, EventCalendar } from "@/components/widgets";
import { Colors, Constants } from "@/theme";
import { ActivityIndicator, Dimensions, View } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { useApi } from "@/hooks";
import { useAuth } from "@/contexts/AuthContext";
import { useState, useCallback } from "react";
import { useFocusEffect } from "expo-router";

export type EventsProps = {
  tabBarHeight?: number;
}

export default function Events ({
  tabBarHeight=0,
}: EventsProps) {

  const insets = useSafeAreaInsets();
  const auth = useAuth();

  const [refresh, setRefresh] = useState(true);

  const { datas: mainDatas, error: mainError, loading: mainLoading, api: getMain } = useApi(true);
  const { datas: champDatas, error: champError, loading: champLoading, api: getChamp } = useApi(true);
  const { datas: calendarDatas, error: calendarError, loading: calendarLoading, api: getCalendar } = useApi(true);

  useFocusEffect(
    useCallback(() => {
      if (auth) {
        getMain({
          endpoint: '/nav/home/main-event?championship_id=1',
          auth: auth
        });
        getChamp({
          endpoint: '/nav/home/championships?championship_id=1',
          auth: auth
        });
        getCalendar({
          endpoint: '/nav/home/events?championship_id=1',
          auth: auth
        });
      }
    }, [auth])
  )

  return (
    <ScrollContainer footerHeight={tabBarHeight} overScrollMode="never">
      {mainDatas && !mainLoading && !mainError && <MainWidget datas={mainDatas} style={{ height: Dimensions.get('window').height - insets.top - tabBarHeight - Constants.spacing.mainWidgetMargin}}/>}
      {champDatas && !champLoading && !champError && <ChampionshipWidget datas={champDatas}/>}
      {calendarDatas && !calendarLoading && !calendarError && <EventCalendar datas={calendarDatas}/>}
      {(calendarLoading || champLoading || mainLoading) && <View style={{ marginVertical: Constants.spacing.mainWidgetMargin }}>
        <ActivityIndicator color={Colors.light.orangeLogo}/>
      </View>}
    </ScrollContainer>
  )
}