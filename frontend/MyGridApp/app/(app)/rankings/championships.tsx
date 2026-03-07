import { Header, MainLoading, RankingsFooter, RankingsList, MainText } from "@/components/widgets";
import { useEffect, useState } from "react";
import { StyleSheet, View } from "react-native";
import { useApi } from "@/hooks";
import { useAuth } from "@/contexts/AuthContext";
import { scopedI18n } from "@/translations/i18n";
import { Colors, GlobalStyles } from "@/theme";

export default function Rankings () {

  const auth = useAuth();
  const t = scopedI18n('rankings');

  const { datas, error, loading, api: getRankings } = useApi(true);

  const [headerHeight, setHeaderHeight] = useState(0);
  const [footerHeight, setFooterHeight] = useState(0);

  useEffect(() => {
    auth && getRankings({
      // Limit should be replaced by paging as soon as possible
      endpoint: `/ranks/championships/1?limit=300`,
      auth: auth
    })
  }, [auth])

  return (
    <View style={{ flex: 1, backgroundColor: Colors.light.background }}>
      <MainLoading loading={loading} color="orange"/>
      {error && <View style={[StyleSheet.absoluteFill, GlobalStyles.container]}>
        <MainText style={{ color: Colors.light.warning }}>{error}</MainText>
      </View>}
      {datas?.ranks && <RankingsList datas={datas.ranks} footerHeight={footerHeight} headerHeight={headerHeight} color={Colors.light.cyanLogo}/>}
      <Header
        onLayout={(e: any) => setHeaderHeight(e.nativeEvent.layout.height)}
        spotColor={Colors.light.cyanLogo}
        title={t('globalRankings')}
        subtitle={t('8events')}
      >
        <MainText style={{ marginBottom: 6, color: Colors.light.warning }}>{t('feature')}</MainText>
      </Header>
      <RankingsFooter
        onLayout={(e: any) => setFooterHeight(e.nativeEvent.layout.height)}
        datas={datas?.viewer_rank}
        spotColor={Colors.light.orangeLogo}
      />
    </View>
  )
}