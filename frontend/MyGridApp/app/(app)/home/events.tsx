import { ScrollContainer, MainWidget, ChampionshipWidget, EventCalendar } from "@/components/widgets";
import { Colors, Constants } from "@/theme";
import { ActivityIndicator, Dimensions, View } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { useApi } from "@/hooks";
import { useAuth } from "@/contexts/AuthContext";
import { useEffect, memo } from "react";

export type EventsProps = {
  tabBarHeight?: number;
}

function Events ({ 
  tabBarHeight=0
}: EventsProps) {

  const insets = useSafeAreaInsets();
  const auth = useAuth()

  const { datas: mainDatas, error: mainError, loading: mainLoading, api: getMain } = useApi(true);
  const { datas: champDatas, error: champError, loading: champLoading, api: getChamp } = useApi(true);
  const { datas: calendarDatas, error: calendarError, loading: calendarLoading, api: getCalendar } = useApi(true);

  useEffect(() => {
    auth && getMain({
      endpoint: '/nav/home/main-event?championship_id=1',
      method: 'GET',
      auth: auth
    })
  }, [auth])

  useEffect(() => {
    auth && !mainLoading && getChamp({
      endpoint: '/nav/home/championships?championship_id=1',
      method: 'GET',
      auth: auth
    })
  }, [mainLoading])

  useEffect(() => {
    auth && !champLoading && getCalendar({
      endpoint: '/nav/home/events?championship_id=1',
      method: 'GET',
      auth: auth
    })
  }, [champLoading])

  return (
    <ScrollContainer footerHeight={tabBarHeight}>
      {mainDatas && !mainLoading && !mainError && <MainWidget datas={mainDatas} style={{ height: Dimensions.get('window').height - insets.top - tabBarHeight - Constants.spacing.mainWidgetMargin}}/>}
      {champDatas && !champLoading && !champError && <ChampionshipWidget datas={champDatas}/>}
      {calendarDatas && !calendarLoading && !calendarError && <EventCalendar datas={calendarDatas}/>}
      {calendarLoading && <View style={{ marginVertical: Constants.spacing.mainWidgetMargin }}>
        <ActivityIndicator color={Colors.light.orangeLogo}/>
      </View>}
    </ScrollContainer>
  )
}

export default memo(Events)