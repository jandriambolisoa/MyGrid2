import { RankingsWidget } from "@/components/widgets";
import { scopedI18n } from "@/translations/i18n";
import { useApi } from "@/hooks";
import { useAuth } from "@/contexts/AuthContext"
import { useEffect } from "react";
import { View, ActivityIndicator } from "react-native";
import { Colors, Constants } from "@/theme";
import { useSafeAreaInsets } from "react-native-safe-area-context";

export default function Social ({
  tabBarHeight=0
}: {
  tabBarHeight?: number;
}) {
  
  const insets = useSafeAreaInsets();
  const t = scopedI18n('home.social');
  const auth = useAuth();
  const margin = Constants.spacing.mainWidgetMargin;

  const { datas: eventDatas, loading: eventLoading, api: getEventRank } = useApi(true);
  const { datas: champDatas, loading: champLoading, api: getChampRank } = useApi(true);
  //const { datas: recordDatas, loading: recordLoading, api: getRecordsRank } = useApi(true);

  useEffect(() => {
    if (auth) {
      getEventRank({
        endpoint: '/nav/social/home/event-rank',
        auth: auth
      });
      getChampRank({
        endpoint: '/nav/social/home/championship-rank?championship_id=1',
        auth: auth
      });
    }
  }, [auth])

  const color1 = eventDatas? eventDatas.event.colors[0] : null;
  const color2 = eventDatas?.event?.colors?.[1] ?? color1;

  return (
    <View style={{
      paddingBottom: tabBarHeight,
      paddingTop: insets.top,
      paddingHorizontal: margin,
      backgroundColor: Colors.light.background,
      flex: 1
    }}>
      {eventDatas && <RankingsWidget
        title={t('weekend')}
        rank={eventDatas.rank}
        score={eventDatas.score}
        color1={color1}
        color2={color2}
        style={{ marginBottom: margin }}
        path='/rankings/events'
      />}
      {champDatas && <RankingsWidget
        title={t('mygrid')}
        rank={champDatas.rank}
        score={champDatas.score}
        color1={Colors.light.cyanLogo}
        color2={Colors.light.orangeLogo}
        style={{ marginBottom: margin }} 
        path='/rankings/championships'
      />}
      <RankingsWidget
        title={t('records')}
        color1={Colors.light.records}
        color2={Colors.light.records}
        style={{ marginBottom: margin }} 
        path='/rankings/records'
      />
      {(eventLoading || champLoading) && <View style={{ marginVertical: Constants.spacing.mainWidgetMargin }}>
        <ActivityIndicator color={Colors.light.orangeLogo}/>
      </View>}
    </View>
  )
}