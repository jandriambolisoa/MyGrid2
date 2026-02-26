import { ScrollContainer, MainWidget, ChampionshipWidget, EventCalendar } from "@/components/widgets";
import { Constants } from "@/theme";
import { Dimensions } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { useApi } from "@/hooks";
import { AuthContext } from "@/contexts/AuthContext";
import { useContext, useEffect } from "react";

// Temporary example datas
/*
import { mainEventDatas } from "./_tmp_main-event"
import { championshipsDatas } from "./_tmp_championships"
import { calendarDatas } from "./_tmp_calendar" */

export type EventsProps = {
  tabBarHeight?: number;
}

export default function Events ({ 
  tabBarHeight=0
}: EventsProps) {

  const insets = useSafeAreaInsets();
  const auth = useContext(AuthContext)

  const { datas: mainDatas, error: mainError, loading: mainLoading, api: getMain } = useApi();
  const { datas: champDatas, error: champError, loading: champLoading, api: getChamp } = useApi();
  const { datas: calendarDatas, error: calendarError, loading: calendarLoading, api: getCalendar } = useApi();

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
    <ScrollContainer tabBarHeight={tabBarHeight}>
      {mainDatas && !mainLoading && !mainError && <MainWidget datas={mainDatas} style={{ height: Dimensions.get('window').height - insets.top - tabBarHeight - Constants.spacing.mainWidgetMargin}}/>}
      {champDatas && !champLoading && !champError && <ChampionshipWidget datas={champDatas}/>}
      {calendarDatas && !calendarLoading && !calendarError && <EventCalendar datas={calendarDatas}/>}
    </ScrollContainer>
  )
}