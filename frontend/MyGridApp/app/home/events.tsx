import { Container, MainWidget, ShadowButton, ChampionshipWidget } from "@/components/widgets";
import { Constants, GlobalStyles } from "@/theme";
import { Dimensions, ScrollView, Image } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";

// Temporary example datas
import { mainEventDatas } from "./_tmp_main-event"
import { championshipsDatas } from "./_tmp_championships"

export type EventsProps = {
  tabBarHeight?: number;
}

export default function Events ({ 
  tabBarHeight=0
}: EventsProps) {

  const insets = useSafeAreaInsets();

  return (
    <Container style={{ paddingBottom: 0, paddingTop: 0 }}>
      <ScrollView style={{ alignSelf: 'stretch' }} contentContainerStyle={{ paddingBottom: tabBarHeight, paddingTop: insets.top }} showsVerticalScrollIndicator={false}>
        <MainWidget datas={JSON.parse(mainEventDatas)} style={{ height: Dimensions.get('window').height - insets.top - tabBarHeight - Constants.spacing.mainWidgetMargin}}/>
        <ShadowButton style={[GlobalStyles.mainWidget]}>
          <Image source={require('@/assets/images/demo/krunker.png')} style={{ height: 100, width: 500 }} resizeMode="stretch"/>
        </ShadowButton>
        <ChampionshipWidget datas={JSON.parse(championshipsDatas)}/>
      </ScrollView>
    </Container>
  )
}