import { Header, ScrollContainer, MainLoading, RankingsFooter } from "@/components/widgets";
import { useEffect, useState } from "react";
import { View } from "react-native";
import { useApi } from "@/hooks";
import { useAuth } from "@/contexts/AuthContext";
import { scopedI18n } from "@/translations/i18n";

export default function Rankings () {

  const auth = useAuth();
  const t = scopedI18n('rankings');

  const { datas, error, loading, api: getRankings } = useApi(true);

  const [headerHeight, setHeaderHeight] = useState(0);
  const [footerHeight, setFooterHeight] = useState(0);

  useEffect(() => {
    auth && getRankings({
      endpoint: `/ranks/events`,
      auth: auth
    })
  }, [auth])

  const color1 = datas?.event.colors[0];
  const color2 = datas?.event.colors.length > 1 ? datas?.session.event.colors[1] : color1;

  return (
    <View style={{ flex: 1 }}>
      <MainLoading loading={loading}/>
      {datas && <ScrollContainer headerHeight={headerHeight} footerHeight={footerHeight}>

      </ScrollContainer>}
      <Header
        onLayout={(e: any) => setHeaderHeight(e.nativeEvent.layout.height)}
        spotColor={color1}
        title={datas?.event.name ? datas.event.name : t('loading')}
        subtitle={t('weekendRankings')}
      >

      </Header>
      <RankingsFooter
        datas={datas?.viewer_rank}
        spotColor={color2}
      />
    </View>
  )
}