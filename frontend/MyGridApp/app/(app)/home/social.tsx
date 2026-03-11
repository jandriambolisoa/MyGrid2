import { RankingsWidget, ScrollContainer } from "@/components/widgets";
import { scopedI18n } from "@/translations/i18n";
import { useApi } from "@/hooks";
import { useAuth } from "@/contexts/AuthContext"
import { useEffect } from "react";
import { View } from "react-native";
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

  const { datas: mainDatas, error: mainError, loading: mainLoading, api: getMain } = useApi(true);

  useEffect(() => {
    auth && getMain({
      endpoint: '/nav/home/main-event?championship_id=1',
      method: 'GET',
      auth: auth
    })
  }, [auth])

  const color1 = mainDatas? mainDatas.event.colors[0] : null;
  const color2 = mainDatas?.event?.colors?.[1] ?? color1;

  return (
    <View style={{
      justifyContent: 'space-evenly',
      paddingBottom: tabBarHeight,
      paddingTop: insets.top,
      paddingHorizontal: margin,
      backgroundColor: Colors.light.background,
      flex: 1
    }}>
      <RankingsWidget
        title={t('weekend')}
        subtitle={t('tapWeekend')}
        color1={color1}
        color2={color2}
        style={{ marginBottom: margin, flex: 1 }}
        path='/rankings/events'
      />
      <RankingsWidget
        title={t('mygrid')}
        subtitle={t('tapMygrid')}
        color1={Colors.light.cyanLogo}
        color2={Colors.light.orangeLogo}
        style={{ marginBottom: margin, flex: 1 }} 
        path='/rankings/championships'
      />
    </View>
  )
}