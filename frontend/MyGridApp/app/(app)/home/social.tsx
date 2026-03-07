import { Container, RankingsWidget } from "@/components/widgets";
import { scopedI18n } from "@/translations/i18n";
import { Dimensions, View } from "react-native";
import { useApi } from "@/hooks";
import { useAuth } from "@/contexts/AuthContext"
import { useEffect } from "react";
import { Colors, Constants, GlobalStyles } from "@/theme";
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

  const { datas: mainDatas, error: mainError, loading: mainLoading, api: getMain } = useApi(true);

  useEffect(() => {
    auth && getMain({
      endpoint: '/nav/home/main-event?championship_id=1',
      method: 'GET',
      auth: auth
    })
  }, [auth])

  const color1 = mainDatas? mainDatas.event.colors[0] : null;
  const color2 = mainDatas?.length > 1 ? mainDatas.event.color[1] : color1;

  return (
    <View style={{
      justifyContent: 'space-evenly',
      alignSelf: 'stretch',
      flex: 1,
      paddingTop: insets.top,
      paddingBottom: tabBarHeight + Constants.spacing.mainWidgetMargin,
      paddingHorizontal: Constants.spacing.mainWidgetMargin,
      backgroundColor: Colors.light.background
    }}>
      <RankingsWidget
        title={t('weekend')}
        subtitle={t('tapWeekend')}
        style={{ marginBottom: Constants.spacing.mainWidgetMargin }}
        color1={color1}
        color2={color2}
        path="/rankings/events"
      />
      <RankingsWidget
        title={t('mygrid')}
        subtitle={t('tapMygrid')}
        color1={Colors.light.cyanLogo}
        color2={Colors.light.orangeLogo}
        path="/rankings/championships"
      />
    </View>
  )
}