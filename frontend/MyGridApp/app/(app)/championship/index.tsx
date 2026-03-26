import { useLocalSearchParams } from "expo-router"
import { View, ActivityIndicator, StyleSheet } from "react-native"
import { Header, ChampionshipList } from "@/components/widgets";
import { useEffect, useState } from "react";
import { useAuth } from "@/contexts/AuthContext";
import { useApi } from "@/hooks";
import { Colors } from "@/theme";
import { scopedI18n } from "@/translations/i18n";

export default function Championship () {

  const { drivers } = useLocalSearchParams();
  const isDrivers = drivers === 'true';

  const t = scopedI18n('championship');
  const auth = useAuth();

  const { datas, loading, api: getChamp } = useApi(true);

  const [headerHeight, setHeaderHeight] = useState(0);

  useEffect(() => {
    auth && getChamp({
      endpoint: isDrivers ? '/nav/standings/drivers?championship_id=1' : '/nav/standings/teams?championship_id=1',
      auth: auth
    })
  }, [auth])

  return (
    <View style={{ flex: 1, backgroundColor: Colors.light.background }}>
      {loading && <View style={[StyleSheet.absoluteFill, { justifyContent: 'center', alignItems: 'center', backgroundColor: Colors.light.background }]}>
        <ActivityIndicator color={Colors.light.orangeLogo}/>
      </View>}
      {datas && <ChampionshipList datas={datas.ranks} headerHeight={headerHeight} drivers={isDrivers}/>}
      <Header
        title={isDrivers ? t('driversChamp') : t('constructorsChamp')}
        spotColor={Colors.light.cyanLogo}
        onLayout={(e) => setHeaderHeight(e.nativeEvent.layout.height)}
      >
        <View style={{ height: 16 }}/>
      </Header>
    </View>
  )
}