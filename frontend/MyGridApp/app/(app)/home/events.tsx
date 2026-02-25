import { ScrollContainer, MainWidget, ChampionshipWidget, EventCalendar } from "@/components/widgets";
import { Constants } from "@/theme";
import { Dimensions } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";

// Temporary example datas
import { mainEventDatas } from "./_tmp_main-event"
import { championshipsDatas } from "./_tmp_championships"
import { calendarDatas } from "./_tmp_calendar"

export type EventsProps = {
  tabBarHeight?: number;
}

export default function Events ({ 
  tabBarHeight=0
}: EventsProps) {

  const insets = useSafeAreaInsets();

  return (
    <ScrollContainer tabBarHeight={tabBarHeight}>
      <MainWidget datas={JSON.parse(mainEventDatas)} style={{ height: Dimensions.get('window').height - insets.top - tabBarHeight - Constants.spacing.mainWidgetMargin}}/>

      <ChampionshipWidget datas={JSON.parse(championshipsDatas)}/>
      <EventCalendar datas={JSON.parse(calendarDatas)}/>
    </ScrollContainer>
  )
}